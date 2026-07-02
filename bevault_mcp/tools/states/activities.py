"""Activity MCP tools."""

import logging

from fastmcp import FastMCP

from ...client.states import StatesClient
from ...models.states import from_api_activities_list_response

logger = logging.getLogger(__name__)


def register_fastmcp(mcp: FastMCP, client: StatesClient) -> None:
    @mcp.tool()
    def get_activities(
        searchString: str | None = None,
        index: int = 0,
        pageSize: int = 10,
    ) -> dict:
        """
        List activities available for Task states in the beVault States module.

        Returns a paginated summary with name and lastContactDate only to keep
        the response compact.

        Args:
            searchString: Optional filter to search activities by name.
            index: Page index (0-based).
            pageSize: Number of results per page.

        Returns:
            A dict with paging info and a list of activity summaries.
        """
        try:
            logger.info(
                "get_activities: searchString=%s, index=%s, pageSize=%s",
                searchString,
                index,
                pageSize,
            )
            api_response = client.activities.list_activities(
                page_size=pageSize,
                index=index,
                search_string=searchString,
            )
            response = from_api_activities_list_response(api_response)
            return response.model_dump(mode="json")
        except Exception:  # noqa: BLE001
            logger.exception("get_activities failed")
            raise
