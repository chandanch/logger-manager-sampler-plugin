from loggermanager import LoggerInterface
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.azure.monitor import AzureMonitorTraceExporter
from opentelemetry.exporter.azure.monitor._metrics import AzureMonitorMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

import os


class AzureAppInsightsLogger(LoggerInterface):
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv(
            "APPLICATIONINSIGHTS_CONNECTION_STRING"
        )
        if not self.connection_string:
            raise ValueError(
                "Azure Application Insights connection string must be provided."
            )

        resource = Resource.create(
            attributes={
                "service.name": "appinsightslogger",
                "service.namespace": "appinsightsdev",
                "service.instance.id": "456-6783-2543-3533",
            }
        )

        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer_provider = trace.get_tracer_provider()
        exporter = AzureMonitorTraceExporter(connection_string=self.connection_string)
        tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
        self.tracer = trace.get_tracer(__name__)

        metrics.set_meter_provider(MeterProvider(resource=resource))
        meter_provider = metrics.get_meter_provider()
        metric_exporter = AzureMonitorMetricExporter(
            connection_string=self.connection_string
        )
        metric_reader = PeriodicExportingMetricReader(exporter=metric_exporter)
        meter_provider._sdk_config.metric_readers.append(metric_reader)
        self.meter = metrics.get_meter(__name__)

    def log_info(self, message: str):
        with self.tracer.start_as_current_span("INFO"):
            print(f"INFO: {message}")

    def log_warning(self, message: str):
        with self.tracer.start_as_current_span("WARNING"):
            print(f"WARNING: {message}")

    def log_error(self, message: str):
        with self.tracer.start_as_current_span("ERROR"):
            print(f"ERROR: {message}")
