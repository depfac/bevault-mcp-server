"""Store MCP tools."""

import logging

from fastmcp.tools import tool

from bevault_mcp.states.client.deps import get_states_client

from bevault_mcp.states.models import from_api_stores_list_response

logger = logging.getLogger(__name__)


client = get_states_client()


@tool()
def get_stores(
    searchString: str | None = None,
    index: int = 0,
    pageSize: int = 10,
) -> dict:
    """
    List stores available for Task states in the beVault States module.

    Returns a paginated summary with name, type, isLocal, environmentName,
    businessDescription, and technicalDescription. Configuration and credentials
    are excluded to avoid exposing sensitive information.

    Args:
        searchString: Optional filter to search stores by name.
        index: Page index (0-based).
        pageSize: Number of results per page.

    Returns:
        A dict with paging info and a list of store summaries.
    """
    try:
        logger.info(
            "get_stores: searchString=%s, index=%s, pageSize=%s",
            searchString,
            index,
            pageSize,
        )
        api_response = client.stores.list_stores(
            page_size=pageSize,
            index=index,
            search_string=searchString,
        )
        response = from_api_stores_list_response(api_response)
        return response.model_dump(mode="json")
    except Exception:  # noqa: BLE001
        logger.exception("get_stores failed")
        raise
