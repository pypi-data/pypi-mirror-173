def instrument():
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()

    # for the exporter
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    span_exporter = OTLPSpanExporter(
        # optional
        endpoint="open-tel:4317",
        insecure=True
        # credentials=ChannelCredentials(credentials),
        # headers=(("metadata", "metadata")),
    )
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Configure the tracer to use the collector exporter
    tracer = trace.get_tracer_provider().get_tracer(__name__)


def instrument_local():
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()

    # for the exporter
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    span_exporter = OTLPSpanExporter(
        # optional
        insecure=True
        # credentials=ChannelCredentials(credentials),
        # headers=(("metadata", "metadata")),
    )
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Configure the tracer to use the collector exporter
    tracer = trace.get_tracer_provider().get_tracer(__name__)
