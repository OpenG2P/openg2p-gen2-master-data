import logging
from openg2p_fastapi_common.controller import BaseController

from ..services import G2PAdminAreaService
from ..helpers import RequestResponseHelper
from ..schemas import (
    GetAllAdministrativeAreaLargeRequest,
    GetAllAdministrativeAreaLargeResponse,
    GetAdministrativeAreaSmallRequest,
    GetAdministrativeAreaSmallResponse,
)
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class G2PAdminAreaController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.router.tags += ["Master Data"]
        self.admin_area_service = G2PAdminAreaService.get_component()
        self.request_response_helper = RequestResponseHelper().get_component()
        self.router.prefix = "/master_data"

        self.router.add_api_route(
            "/get_all_administrative_area_large",
            self.get_all_administrative_area_large,
            responses={200: {"model": GetAllAdministrativeAreaLargeResponse}},
            methods=["POST"],
        )

        self.router.add_api_route(
            "/get_administrative_area_small_for_large_area",
            self.get_administrative_area_small_for_large_area,
            responses={200: {"model": GetAdministrativeAreaSmallResponse}},
            methods=["POST"],
        )

    async def get_all_administrative_area_large(
        self,
        get_all_administrative_area_large_request: GetAllAdministrativeAreaLargeRequest,
    ) -> GetAllAdministrativeAreaLargeResponse:
        _logger.debug("Get Administrative Area Large Request: %s", get_all_administrative_area_large_request)
        try:
            administrative_area_large_list = await self.admin_area_service.get_all_administrative_area_large()

            _logger.debug("Administrative areas large: %s", administrative_area_large_list)

            return self.request_response_helper.construct_success_response_large(
                get_all_administrative_area_large_request, administrative_area_large_list
            )
        except Exception as e:
            _logger.error("Error getting administrative area large: %s", str(e), exc_info=True)
            return self.request_response_helper.construct_error_response_large(e, get_all_administrative_area_large_request)

    async def get_administrative_area_small_for_large_area(
        self,
        request: GetAdministrativeAreaSmallRequest,
    ) -> GetAdministrativeAreaSmallResponse:
        _logger.debug("Get Administrative Area Small Request: %s", request)
        try:
            areas = await self.admin_area_service.get_administrative_area_small_for_large_area(
                request.request_body.request_payload.administrative_area_large_id
            )

            _logger.debug("Administrative areas small: %s", areas)

            return self.request_response_helper.construct_success_response_small(
                request, areas
            )
        except Exception as e:
            _logger.error("Error getting administrative area small: %s", str(e), exc_info=True)
            return self.request_response_helper.construct_error_response_small(e, request)
