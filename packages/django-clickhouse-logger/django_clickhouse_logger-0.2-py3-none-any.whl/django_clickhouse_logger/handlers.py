import logging
from logging import StreamHandler

from django_clickhouse_logger import clickhouse
from django.core.handlers.wsgi import WSGIRequest


class ClickhouseLoggerHandler(StreamHandler):

    def emit(self, record) -> None:
        if isinstance(record, logging.LogRecord) and getattr(record, 'request', False) and isinstance(record.request, WSGIRequest):
            clickhouse.proxy(record)


