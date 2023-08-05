from netlink.sap.monitor import transactional_rfc_calls
from netlink.datadog.core import GaugeMetric
import datetime


def rfc_transactional_calls(rfc_connection, datadog_queue, tags=None):
    timestamp = int(datetime.datetime.now().timestamp())
    data = transactional_rfc_calls(rfc_connection)
    tags = {f"sap_sid:{rfc_connection.sysid}", f"sap_client:{rfc_connection.client}", "sap_type:abap"}.union(
        tags or set()
    )

    gauge_metric = GaugeMetric(
        "netlink_sap.abap.rfc.transactional.calls", host=rfc_connection.hostname, source="netlink_sap", tags=tags
    )

    for age in data:
        for destination in data[age]:
            for state in data[age][destination]:
                for function_module in data[age][destination][state]:
                    for user in data[age][destination][state][function_module]:
                        for tcode in data[age][destination][state][function_module][user]:
                            datadog_queue.put(
                                gauge_metric.metric(
                                    timestamp,
                                    data[age][destination][state][function_module][user][tcode],
                                    tags={
                                        f"sap_age_bracket:{age}",
                                        f"sap_rfc_destination:{destination}",
                                        f"sap_trfc_status:{state}",
                                        f"sap_function_module:{function_module}",
                                        f"sap_user:{user}",
                                        f"sap_transaction_code:{tcode}",
                                    },
                                )
                            )
