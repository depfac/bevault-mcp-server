"""OpenTelemetry initialization with environment variable configuration."""

import os

from dotenv import load_dotenv


def _init_otel() -> None:
    """
    Initialize OpenTelemetry SDK when OTEL_EXPORTER_OTLP_ENDPOINT is set.

    Configuration via environment variables:
    - OTEL_EXPORTER_OTLP_ENDPOINT: OTLP collector endpoint (required for activation)
    - OTEL_SERVICE_NAME: Service name in traces (default: bevault-mcp)

    Must be called before importing FastMCP.
    """
    load_dotenv()

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if not endpoint:
        return

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource

    service_name = os.getenv("OTEL_SERVICE_NAME", "bevault-mcp").strip()
    exporter = OTLPSpanExporter(endpoint=endpoint)
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


# Run on module import so tracer is configured before FastMCP is loaded
_init_otel()
