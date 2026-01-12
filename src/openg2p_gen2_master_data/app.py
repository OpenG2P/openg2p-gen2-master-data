# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .controllers import G2PAdminAreaController
from .models import G2PAdministrativeAreaLarge, G2PAdministrativeAreaSmall
from .helpers import RequestResponseHelper

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        RequestResponseHelper()
        G2PAdminAreaController().post_init()

    def migrate_database(self, args):
        _logger.info("Starting database migration")

        async def migrate():
            await G2PAdministrativeAreaLarge.create_migrate()
            await G2PAdministrativeAreaSmall.create_migrate()
            _logger.info("Database migration completed")

        asyncio.run(migrate())
