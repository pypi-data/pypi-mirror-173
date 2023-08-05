import time

from netlink.logging import logger
import threading as threading
import queue as queue
from netlink.sap.rfc import dest


class AbapWorker(threading.Thread):
    def __init__(
        self,
        i: int,
        destination: str,
        queue: queue.SimpleQueue,
        datadog_queue: queue.SimpleQueue,
        shutdown_event: threading.Event,
        tags: list,
        *args,
        **kwargs,
    ):
        super(AbapWorker, self).__init__(name=f"{destination}-{i}", *args, **kwargs)
        self.destination = destination
        self.queue = queue
        self.shutdown_event = shutdown_event
        self.tags = tags
        self.datadog_queue = datadog_queue

    def run(self):
        logger.debug(f"Starting ABAP Worker {self.name} ({self.native_id})")
        self.rfc_connection = dest(self.destination)
        while not self.shutdown_event.is_set():
            try:
                item = self.queue.get(timeout=1)
            except queue.Empty:
                time.sleep(1)
            else:
                logger.debug(f"calling {item}")
                if not self.rfc_connection.is_alive:
                    self.rfc_connection.open()
                item(self.rfc_connection, self.datadog_queue, self.tags)
                self.rfc_connection.reset_server_context()
        self.rfc_connection.close()

    def __del__(self):
        try:
            self.rfc_connection.close()
        except:
            pass
