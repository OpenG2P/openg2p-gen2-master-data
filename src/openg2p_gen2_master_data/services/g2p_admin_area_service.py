import logging
from typing import List
from sqlalchemy import select
from openg2p_fastapi_common.service import BaseService

from ..engine import get_session_maker
from ..models import G2PAdministrativeAreaLarge, G2PAdministrativeAreaSmall
from ..schemas import (
    AdministrativeAreaLargeData,
    AdministrativeAreaSmallData,
)

_config = None
try:
    from ..config import Settings
    _config = Settings.get_config()
except Exception:
    pass

_logger = logging.getLogger(_config.logging_default_logger_name if _config else "g2p-admin_area-service")


class G2PAdminAreaService(BaseService):
    async def get_all_administrative_area_large(self) -> List[AdministrativeAreaLargeData]:
        """
        Get all administrative area large records.
        
        Returns:
            List of AdministrativeAreaLargeData
        """
        async with get_session_maker()() as session:
            areas = (await session.execute(select(G2PAdministrativeAreaLarge))).scalars().all()
            
            return [
                AdministrativeAreaLargeData(
                    area_id=area.area_id,
                    area_mnemonic=area.area_mnemonic,
                    area_description=area.area_description,
                )
                for area in areas
            ]

    async def get_administrative_area_small_for_large_area(self, administrative_area_large_id: str ) -> List[AdministrativeAreaSmallData]:
        """
        Get all administrative area small records with their related large area information.
        
        Returns:
            List of AdministrativeAreaSmallData
        """
        async with get_session_maker()() as session:
            
            query = (
                select(G2PAdministrativeAreaSmall, G2PAdministrativeAreaLarge)
                .join(
                    G2PAdministrativeAreaLarge,
                    G2PAdministrativeAreaSmall.administrative_area_large_id == G2PAdministrativeAreaLarge.area_id,
                )
                .where(G2PAdministrativeAreaSmall.administrative_area_large_id == administrative_area_large_id)
            )
            
            result = await session.execute(query)
            rows = result.all()
            
            return [
                AdministrativeAreaSmallData(
                    area_id=small.area_id,
                    area_mnemonic=small.area_mnemonic,
                    area_description=small.area_description,
                    administrative_area_large_id=small.administrative_area_large_id,
                    administrative_area_large_mnemonic=large.area_mnemonic,
                    administrative_area_large_description=large.area_description,
                )
                for small, large in rows
            ]
