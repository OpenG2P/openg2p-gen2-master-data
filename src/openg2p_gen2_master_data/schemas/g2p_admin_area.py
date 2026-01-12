from typing import Optional, List
from pydantic import BaseModel
from openg2p_fastapi_common.schemas import (
    G2PRequest,
    G2PRequestBody,
    G2PResponse,
    G2PResponseBody,
    G2PResponseHeader,
    G2PResponseStatus,
)


# Administrative Area Large Request/Response
class GetAdministrativeAreaLargeRequestPayload(BaseModel):
    administrative_area_large_id: Optional[str] = None


class GetAdministrativeAreaLargeRequestBody(G2PRequestBody):
    request_payload: GetAdministrativeAreaLargeRequestPayload


class GetAdministrativeAreaLargeRequest(G2PRequest):
    request_body: GetAdministrativeAreaLargeRequestBody


class AdministrativeAreaLargeData(BaseModel):
    area_id: str
    area_mnemonic: str
    area_description: str


class GetAdministrativeAreaLargeResponseBody(G2PResponseBody):
    response_payload: List[AdministrativeAreaLargeData]


class GetAdministrativeAreaLargeResponse(G2PResponse):
    response_header: G2PResponseHeader
    response_body: GetAdministrativeAreaLargeResponseBody


# Administrative Area Small Request/Response
class GetAdministrativeAreaSmallRequestPayload(BaseModel):
    pass


class GetAdministrativeAreaSmallRequestBody(G2PRequestBody):
    request_payload: GetAdministrativeAreaSmallRequestPayload


class GetAdministrativeAreaSmallRequest(G2PRequest):
    request_body: GetAdministrativeAreaSmallRequestBody


class AdministrativeAreaSmallData(BaseModel):
    area_id: str
    area_mnemonic: str
    area_description: str
    administrative_area_large_id: str
    administrative_area_large_mnemonic: str
    administrative_area_large_description: str


class GetAdministrativeAreaSmallResponseBody(G2PResponseBody):
    response_payload: List[AdministrativeAreaSmallData]


class GetAdministrativeAreaSmallResponse(G2PResponse):
    response_header: G2PResponseHeader
    response_body: GetAdministrativeAreaSmallResponseBody
