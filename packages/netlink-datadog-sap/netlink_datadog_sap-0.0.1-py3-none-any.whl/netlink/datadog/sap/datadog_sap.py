import collections
import queue
import threading
import time
from netlink.logging import logger
from netlink.datadog.core import Worker as DatadogWorker
import schedule
from .abap_worker import AbapWorker
from ..sap import abap as abap_checks
import inspect
import pathlib

checks = {name: obj for name, obj in inspect.getmembers(abap_checks) if inspect.isfunction(obj)}

stop_semaphore = pathlib.Path("stop")


def schedule_check(queue, check):
    queue.put(check)


class DatadogSapMonitor:
    def __init__(self, datadog_configuration, abap_configuration):
        self.datadog_configuration = datadog_configuration
        self.abap_configuration = abap_configuration

        self.shutdown_event = threading.Event()
        self.datadog_workers = []
        self.datadog_queue = queue.SimpleQueue()

        self.abap_workers = collections.defaultdict(list)
        self.abap_queues = {}

    def start(self):
        logger.verbose(f"Starting datadog {self.datadog_configuration['workers']} worker(s)")
        for i in range(self.datadog_configuration["workers"]):
            self.datadog_workers.append(
                DatadogWorker(
                    i,
                    self.datadog_configuration["api_key"],
                    self.datadog_configuration["site"],
                    self.datadog_queue,
                    self.shutdown_event,
                )
            )
        for i in self.datadog_workers:
            i.start()

        logger.verbose(f"Starting ABAP worker(s)")
        for k, v in self.abap_configuration.items():
            self.abap_queues[k] = queue.SimpleQueue()
            for i in range(v.get("workers", 1)):

                self.abap_workers[k].append(
                    AbapWorker(
                        i,
                        k,
                        self.abap_queues[k],
                        self.datadog_queue,
                        self.shutdown_event,
                        self.datadog_configuration["tags"],
                    )
                )
            for i in self.abap_workers[k]:
                logger.debug(f"{k} {i}")
                i.start()

        logger.verbose(f"Scheduling checks")
        for k, v in self.abap_configuration.items():
            for c in v["checks"]:
                h, m, s = v["checks"][c]["frequency"].split(":")
                seconds = (((int(h) * 60) + int(m)) * 60) + int(s)
                logger.verbose(f"scheduling {c} every {v['checks'][c]['frequency']} for {k}")
                schedule.every(seconds).seconds.do(schedule_check, queue=self.abap_queues[k], check=checks[c])
                self.abap_queues[k].put(checks[c])

        logger.verbose(f"running schedule")
        while True:
            if stop_semaphore.exists():
                stop_semaphore.unlink()
                self.shutdown_event.set()
                break
            schedule.run_pending()
            time.sleep(1)
