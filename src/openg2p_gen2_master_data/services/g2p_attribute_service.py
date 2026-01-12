import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from openg2p_fastapi_common.service import BaseService
from openg2p_fastapi_common.context import dbengine

from ..models import G2PAttributeValue, G2PAdministrativeAreaLarge, G2PAdministrativeAreaSmall
from ..schemas import (
    G2PAttributeValueData,
    AdministrativeAreaLargeData,
    AdministrativeAreaSmallData,
)

_config = None
try:
    from ..config import Settings
    _config = Settings.get_config()
except Exception:
    pass

_logger = logging.getLogger(_config.logging_default_logger_name if _config else "g2p-attribute-service")


class G2PAttributeService(BaseService):
    async def get_attribute_values(
        self,
        attribute_id: str,
        parent_value_id: Optional[str] = None,
    ) -> List[G2PAttributeValueData]:
        """
        Get attribute values for a given attribute_id.
        If parent_value_id is provided, returns only values with that parent.
        If parent_value_id is None, returns all values for the attribute (top-level if hierarchical).
        
        Args:
            attribute_id: The attribute ID to get values for
            parent_value_id: Optional parent value ID to filter by
            
        Returns:
            List of G2PAttributeValueData sorted by sort_order
        """
        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        
        async with session_maker() as session:
            # Build query
            query = select(G2PAttributeValue).where(
                G2PAttributeValue.attribute_id == attribute_id
            )
            
            # Filter by parent_value_id if provided
            if parent_value_id is not None:
                query = query.where(G2PAttributeValue.parent_value_id == parent_value_id)
            else:
                # If parent_value_id is None, get top-level values (where parent_value_id is NULL)
                query = query.where(G2PAttributeValue.parent_value_id.is_(None))
            
            # Order by sort_order
            query = query.order_by(G2PAttributeValue.sort_order)
            
            # Execute query
            result = await session.execute(query)
            attribute_values = result.scalars().all()
            
            # Convert to response data
            return [
                G2PAttributeValueData(
                    value_id=value.value_id,
                    attribute_id=value.attribute_id,
                    value_code=value.value_code,
                    value_display=value.value_display,
                    parent_value_id=value.parent_value_id,
                    sort_order=value.sort_order,
                )
                for value in attribute_values
            ]

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
