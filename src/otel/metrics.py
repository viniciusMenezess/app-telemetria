from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import random
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation
import os

APP_NAME = os.getenv("APP_NAME", "app-a")

prometheus_reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader]))

meter = metrics.get_meter(APP_NAME)

request_counter = meter.create_counter(
    name = "app_requests_total",
    description = "Total de requisições processadas",
    unit = "1"
)

def get_random_value(options: CallbackOptions) -> Iterable[Observation]:
    value = random.randint(0, 100)
    yield Observation(value, {"service": APP_NAME})

random_value = meter.create_observable_counter(
    name="app_random_values_total",
    description="Total de valores aleatórios gerados",
    callbacks=[get_random_value]
)