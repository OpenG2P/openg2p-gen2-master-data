from datetime import datetime
from typing import List
from openg2p_fastapi_common.service import BaseService
from openg2p_fastapi_common.schemas import G2PRequest, G2PResponseHeader, G2PResponseStatus, G2PResponseBody

from ..schemas import (
    GetAdministrativeAreaLargeRequest,
    GetAdministrativeAreaLargeResponse,
    GetAdministrativeAreaLargeResponseBody,
    AdministrativeAreaLargeData,
    GetAdministrativeAreaSmallRequest,
    GetAdministrativeAreaSmallResponse,
    GetAdministrativeAreaSmallResponseBody,
    AdministrativeAreaSmallData,
)


class RequestResponseHelper(BaseService):
    def construct_success_response_large(
        self,
        g2p_request: GetAdministrativeAreaLargeRequest,
        areas: List[AdministrativeAreaLargeData],
    ) -> GetAdministrativeAreaLargeResponse:
        """
        Construct a success response for get_administrative_area_large API.
        
        Args:
            g2p_request: The G2P request object
            areas: List of administrative area large data to return
            
        Returns:
            GetAdministrativeAreaLargeResponse with success status
        """
        request_id = g2p_request.request_header.request_id if g2p_request.request_header else ""

        response_header = G2PResponseHeader(
            request_id=request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code="",
            response_error_message="",
            response_timestamp=datetime.now(),
        )

        response_body = GetAdministrativeAreaLargeResponseBody(
            pagination_response=None,
            response_payload=areas,
        )

        return GetAdministrativeAreaLargeResponse(
            response_header=response_header,
            response_body=response_body,
        )

    def construct_error_response_large(
        self,
        error: Exception,
        g2p_request: GetAdministrativeAreaLargeRequest = None,
    ) -> GetAdministrativeAreaLargeResponse:
        """
        Construct an error response for get_administrative_area_large API.
        
        Args:
            error: The exception that occurred
            g2p_request: Optional G2P request object
            
        Returns:
            GetAdministrativeAreaLargeResponse with error status
        """
        if hasattr(error, "code") and hasattr(error, "message"):
            error_code = str(error.code)
            error_message = error.message
        else:
            error_code = "500"
            error_message = str(error)

        request_id = ""
        if g2p_request and g2p_request.request_header:
            request_id = g2p_request.request_header.request_id

        response_header = G2PResponseHeader(
            request_id=request_id,
            response_status=G2PResponseStatus.ERROR,
            response_error_code=error_code,
            response_error_message=error_message,
            response_timestamp=datetime.now(),
        )

        response_body = G2PResponseBody(
            pagination_response=None,
            response_payload=None,
        )

        return GetAdministrativeAreaLargeResponse(
            response_header=response_header,
            response_body=response_body,
        )

    def construct_success_response_small(
        self,
        g2p_request: GetAdministrativeAreaSmallRequest,
        areas: List[AdministrativeAreaSmallData],
    ) -> GetAdministrativeAreaSmallResponse:
        """
        Construct a success response for get_administrative_area_small API.
        
        Args:
            g2p_request: The G2P request object
            areas: List of administrative area small data to return
            
        Returns:
            GetAdministrativeAreaSmallResponse with success status
        """
        request_id = g2p_request.request_header.request_id if g2p_request.request_header else ""

        response_header = G2PResponseHeader(
            request_id=request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code="",
            response_error_message="",
            response_timestamp=datetime.now(),
        )

        response_body = GetAdministrativeAreaSmallResponseBody(
            pagination_response=None,
            response_payload=areas,
        )

        return GetAdministrativeAreaSmallResponse(
            response_header=response_header,
            response_body=response_body,
        )

    def construct_error_response_small(
        self,
        error: Exception,
        g2p_request: GetAdministrativeAreaSmallRequest = None,
    ) -> GetAdministrativeAreaSmallResponse:
        """
        Construct an error response for get_administrative_area_small API.
        
        Args:
            error: The exception that occurred
            g2p_request: Optional G2P request object
            
        Returns:
            GetAdministrativeAreaSmallResponse with error status
        """
        if hasattr(error, "code") and hasattr(error, "message"):
            error_code = str(error.code)
            error_message = error.message
        else:
            error_code = "500"
            error_message = str(error)

        request_id = ""
        if g2p_request and g2p_request.request_header:
            request_id = g2p_request.request_header.request_id

        response_header = G2PResponseHeader(
            request_id=request_id,
            response_status=G2PResponseStatus.ERROR,
            response_error_code=error_code,
            response_error_message=error_message,
            response_timestamp=datetime.now(),
        )

        response_body = G2PResponseBody(
            pagination_response=None,
            response_payload=None,
        )

        return GetAdministrativeAreaSmallResponse(
            response_header=response_header,
            response_body=response_body,
        )
