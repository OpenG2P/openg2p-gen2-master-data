# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .controllers import G2PAttributeController
from .helpers import RequestResponseHelper

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        RequestResponseHelper()
        G2PAttributeController().post_init()

    def migrate_database(self, args):
        _logger.info("Starting database migration")

        # TODO: Add any database migration code here
        _logger.info("Database migration completed")
