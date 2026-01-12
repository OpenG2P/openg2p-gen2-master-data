import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from openg2p_fastapi_common.service import BaseService
from openg2p_fastapi_common.context import dbengine

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
    async def get_administrative_area_large(
        self,
        administrative_area_large_id: Optional[str] = None,
    ) -> List[AdministrativeAreaLargeData]:
        """
        Get administrative area large records.
        If administrative_area_large_id is provided, returns only that record.
        If not provided, returns all records.
        
        Args:
            administrative_area_large_id: Optional area ID to filter by
            
        Returns:
            List of AdministrativeAreaLargeData
        """
        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        
        async with session_maker() as session:
            query = select(G2PAdministrativeAreaLarge)
            
            if administrative_area_large_id is not None:
                query = query.where(
                    G2PAdministrativeAreaLarge.area_id == administrative_area_large_id
                )
            
            result = await session.execute(query)
            areas = result.scalars().all()
            
            return [
                AdministrativeAreaLargeData(
                    area_id=area.area_id,
                    area_mnemonic=area.area_mnemonic,
                    area_description=area.area_description,
                )
                for area in areas
            ]

    async def get_administrative_area_small(
        self,
    ) -> List[AdministrativeAreaSmallData]:
        """
        Get all administrative area small records with their related large area information.
        
        Returns:
            List of AdministrativeAreaSmallData
        """
        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        
        async with session_maker() as session:
            # Join with large area to get related fields
            query = select(
                G2PAdministrativeAreaSmall,
                G2PAdministrativeAreaLarge
            ).join(
                G2PAdministrativeAreaLarge,
                G2PAdministrativeAreaSmall.administrative_area_large_id == G2PAdministrativeAreaLarge.area_id
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
