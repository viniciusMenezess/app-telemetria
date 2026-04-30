from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.view import View
from opentelemetry.sdk.metrics._internal.aggregation import ExplicitBucketHistogramAggregation
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import random
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation
import psutil
import os

APP_NAME = os.getenv("APP_NAME", "app-a")

response_time_view = View(
    instrument_name="app_response_time",
    aggregation=ExplicitBucketHistogramAggregation(boundaries=[0.1, 0.5, 1, 2.5, 5, 10])
)

prometheus_reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader], views=[response_time_view]))

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

active_requests_gauge = meter.create_gauge (
    name="app_active_requests",
    description="Número de requisições ativas",
    unit="1"
)

process = psutil.Process()

# FUnção para obter uso de memória do processo
def get_memory_usage(options: CallbackOptions) -> Iterable[Observation]:
    memory_info = process.memory_info()
    memory_usage = memory_info.rss  # Uso de memória em bytes
    yield Observation(memory_usage, {"service": APP_NAME})

memory_gauge = meter.create_observable_gauge(
    name="app_memory_usage",
    description="Uso de memória do processo em bytes",
    callbacks=[get_memory_usage]
)

#METRICA DE HISTOGRAMA PARA TEMPO DE RESPOSTA

response_time_histogram = meter.create_histogram(
    name="app_response_time",
    description="Tempo de resposta das requisições",
    unit="s",
)