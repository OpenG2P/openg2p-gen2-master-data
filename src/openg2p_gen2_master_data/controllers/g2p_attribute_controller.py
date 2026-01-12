import logging
from openg2p_fastapi_common.controller import BaseController

from ..services import G2PAttributeService
from ..helpers import RequestResponseHelper
from ..schemas import (
    GetG2PAttributeValuesRequest,
    GetG2PAttributeValuesResponse,
    GetAdministrativeAreaLargeRequest,
    GetAdministrativeAreaLargeResponse,
    GetAdministrativeAreaSmallRequest,
    GetAdministrativeAreaSmallResponse,
)
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class G2PAttributeController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.router.tags += ["Master Data"]
        self.attribute_service = G2PAttributeService().get_component()
        self.request_response_helper = RequestResponseHelper().get_component()
        self.router.prefix = "/master_data"

        self.router.add_api_route(
            "/get_g2p_attribute_values",
            self.get_g2p_attribute_values,
            responses={200: {"model": GetG2PAttributeValuesResponse}},
            methods=["POST"],
        )

        self.router.add_api_route(
            "/get_administrative_area_large",
            self.get_administrative_area_large,
            responses={200: {"model": GetAdministrativeAreaLargeResponse}},
            methods=["POST"],
        )

        self.router.add_api_route(
            "/get_administrative_area_small",
            self.get_administrative_area_small,
            responses={200: {"model": GetAdministrativeAreaSmallResponse}},
            methods=["POST"],
        )

    async def get_g2p_attribute_values(
        self,
        request: GetG2PAttributeValuesRequest,
    ) -> GetG2PAttributeValuesResponse:
        _logger.debug("Get G2P Attribute Values Request: %s", request)
        try:
            request_payload = request.request_body.request_payload
            attribute_values = await self.attribute_service.get_attribute_values(
                attribute_id=request_payload.attribute_id,
                parent_value_id=request_payload.parent_value_id,
            )

            _logger.debug("Attribute values: %s", attribute_values)

            return self.request_response_helper.construct_success_response(
                request, attribute_values
            )
        except Exception as e:
            _logger.error("Error getting attribute values: %s", str(e), exc_info=True)
            return self.request_response_helper.construct_error_response(e, request)

    async def get_administrative_area_large(
        self,
        request: GetAdministrativeAreaLargeRequest,
    ) -> GetAdministrativeAreaLargeResponse:
        _logger.debug("Get Administrative Area Large Request: %s", request)
        try:
            request_payload = request.request_body.request_payload
            areas = await self.attribute_service.get_administrative_area_large(
                administrative_area_large_id=request_payload.administrative_area_large_id,
            )

            _logger.debug("Administrative areas large: %s", areas)

            return self.request_response_helper.construct_success_response_large(
                request, areas
            )
        except Exception as e:
            _logger.error("Error getting administrative area large: %s", str(e), exc_info=True)
            return self.request_response_helper.construct_error_response_large(e, request)

    async def get_administrative_area_small(
        self,
        request: GetAdministrativeAreaSmallRequest,
    ) -> GetAdministrativeAreaSmallResponse:
        _logger.debug("Get Administrative Area Small Request: %s", request)
        try:
            areas = await self.attribute_service.get_administrative_area_small()

            _logger.debug("Administrative areas small: %s", areas)

            return self.request_response_helper.construct_success_response_small(
                request, areas
            )
        except Exception as e:
            _logger.error("Error getting administrative area small: %s", str(e), exc_info=True)
            return self.request_response_helper.construct_error_response_small(e, request)
