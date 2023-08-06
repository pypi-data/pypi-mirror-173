#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: implement server connection

import logging
import json
from .utils import (
    get_timestamp_ms,
    remove_empty_keys,
)
import inspect
from os import environ

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(message)s')


class Binnakle:
    def __init__(
        self,
        pretty: bool = None,
        env: str = None,
        prefix: str = None,
        server_url: str = None,
        name: str = None,
    ):
        if pretty is None:
            self._pretty = environ.get(
                'BINNAKLE_PRETTY',
                'false',
            ).lower() == 'true'
        else:
            self._pretty = pretty

        if env is None:
            self._env = environ.get(
                'BINNAKLE_ENV',
                'local',
            ).lower()
        else:
            self._env = env

        self._server_url = server_url
        self._prefix = prefix
        self._name = name

        self._logger = logging.getLogger(self._name)

    def set_level(
        self,
        level: str = None,
        name: str = None,
    ):
        if level is None:
            raise ValueError('level is required')
        logging.getLogger(name).setLevel(getattr(logging, level.upper()))

    def wrapped(method):
        def _wrapped(self, message, *args, **kwargs):
            if self._prefix is not None:
                message = self._prefix + message

            inspection = inspect.stack()[1]
            message_dict = remove_empty_keys(
                {
                    'level': method.__name__,
                    'message': message,
                    'timestamp': get_timestamp_ms(),
                    'env': self._env,
                    'filepath': inspection.filename,
                    'function': inspection.function,
                    'line': inspection.lineno
                }
            )

            modified_message = json.dumps(
                message_dict,
                indent=4 if self._pretty else None,
                separators=None if self._pretty else (',',
                                                      ':'),
                ensure_ascii=False,
            )
            return method(self, modified_message)

        return _wrapped

    @wrapped
    def info(self, msg):
        self._logger.info(msg)

    @wrapped
    def error(self, msg):
        self._logger.error(msg)

    @wrapped
    def warning(self, msg):
        self._logger.warning(msg)

    @wrapped
    def warn(self, msg):
        self._logger.warning(msg)

    @wrapped
    def debug(self, msg):
        self._logger.debug(msg)

    @wrapped
    def critical(self, msg):
        self._logger.critical(msg)

    @wrapped
    def exception(self, msg):
        self._logger.exception(msg)
