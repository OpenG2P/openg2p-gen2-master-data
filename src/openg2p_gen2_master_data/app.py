# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .controllers import G2PAdminAreaController, G2PPartnerController
from .models import G2PAdministrativeAreaLarge, G2PAdministrativeAreaSmall, G2PPartner
from .helpers import RequestResponseHelper

from .services import G2PAdminAreaService, G2PPartnerService

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        RequestResponseHelper()

        G2PAdminAreaService()
        G2PPartnerService()
        
        G2PAdminAreaController().post_init()
        G2PPartnerController().post_init()

    def migrate_database(self, args):
        _logger.info("Starting database migration")

        async def migrate():
            await G2PAdministrativeAreaLarge.create_migrate()
            await G2PAdministrativeAreaSmall.create_migrate()
            await G2PPartner.create_migrate()
            _logger.info("Database migration completed")

        asyncio.run(migrate())
