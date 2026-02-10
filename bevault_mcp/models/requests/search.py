"""Search request parameters."""

from typing import Optional

from pydantic import BaseModel


class SearchParams(BaseModel):
    """Parameters for searching model entities."""

    searchString: str
    projectName: Optional[str] = None
    index: int = 0
    limit: int = 10
    includeHubs: bool = True
    includeLinks: bool = True
    includeSatellites: bool = True
    includeReferenceTables: bool = True
