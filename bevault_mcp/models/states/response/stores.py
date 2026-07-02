"""Optimized store MCP response models."""

from pydantic import BaseModel

from ..api import StoreListItem, StoresListResponse
from .state_machines import StatesPagingInfo


class StoreSummary(BaseModel):
    """Trimmed store summary for list responses."""

    name: str
    type: str
    isLocal: bool
    environmentName: str | None = None
    businessDescription: str | None = None
    technicalDescription: str | None = None


class ListStoresResponse(BaseModel):
    """Optimized get_stores MCP tool response."""

    paging: StatesPagingInfo
    stores: list[StoreSummary]


def from_api_stores_list_response(
    api_response: StoresListResponse,
) -> ListStoresResponse:
    """Convert a States API list response to an optimized MCP response."""
    page_size = api_response.pageSize
    if page_size is None:
        page_size = len(api_response.results)

    return ListStoresResponse(
        paging=StatesPagingInfo(
            totalCount=api_response.totalCount,
            pageSize=page_size,
            index=api_response.index,
        ),
        stores=[_to_summary(item) for item in api_response.results],
    )


def _to_summary(item: StoreListItem) -> StoreSummary:
    return StoreSummary(
        name=item.name,
        type=item.type,
        isLocal=item.source is not None,
        environmentName=(
            item.source.workerServiceEnvironmentName if item.source else None
        ),
        businessDescription=item.businessDescription,
        technicalDescription=item.technicalDescription,
    )
