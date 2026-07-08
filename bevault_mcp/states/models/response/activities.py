"""Optimized activity MCP response models."""

from pydantic import BaseModel

from ..api import ActivitiesListResponse, ActivityListItem
from .state_machines import StatesPagingInfo


class ActivitySummary(BaseModel):
    """Trimmed activity summary for list responses."""

    name: str
    lastContactDate: str | None = None


class ListActivitiesResponse(BaseModel):
    """Optimized get_activities MCP tool response."""

    paging: StatesPagingInfo
    activities: list[ActivitySummary]


def from_api_activities_list_response(
    api_response: ActivitiesListResponse,
) -> ListActivitiesResponse:
    """Convert a States API list response to an optimized MCP response."""
    return ListActivitiesResponse(
        paging=StatesPagingInfo(
            totalCount=api_response.totalCount,
            pageSize=api_response.pageSize,
            index=api_response.index,
        ),
        activities=[_to_summary(item) for item in api_response.results],
    )


def _to_summary(item: ActivityListItem) -> ActivitySummary:
    return ActivitySummary(
        name=item.name,
        lastContactDate=item.lastContact,
    )
