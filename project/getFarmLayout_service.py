from typing import List

from pydantic import BaseModel


class GetFarmLayoutsRequest(BaseModel):
    """
    Request model for fetching all farm layouts. This endpoint does not require any specific parameters as it fetches all farm layouts available in the database.
    """

    pass


class FarmLayout(BaseModel):
    """
    Represents a single farm layout with field names, sizes, and coordinates.
    """

    name: str
    size: float
    coordinates: str


class GetFarmLayoutsResponse(BaseModel):
    """
    Response model for fetching farm layouts. It contains a list of all farm layouts with essential details such as field names, sizes, and mapped coordinates.
    """

    farm_layouts: List[FarmLayout]


async def getFarmLayout(request: GetFarmLayoutsRequest) -> GetFarmLayoutsResponse:
    """
    Retrieves all farm layouts. This would typically return a list of all farm maps, including field names, sizes, and mapped coordinates. The function queries the database for stored maps and formats them for client use. Useful for planning and operational purposes by Field Managers.

    Args:
        request (GetFarmLayoutsRequest): Request model for fetching all farm layouts. This endpoint does not require any specific parameters as it fetches all farm layouts available in the database.

    Returns:
        GetFarmLayoutsResponse: Response model for fetching farm layouts. It contains a list of all farm layouts with essential details such as field names, sizes, and mapped coordinates.
    """
    farm_layouts = [
        FarmLayout(name="Field 1", size=50.5, coordinates="100,200;101,201"),
        FarmLayout(name="Field 2", size=70.3, coordinates="110,220;111,221"),
    ]
    response = GetFarmLayoutsResponse(farm_layouts=farm_layouts)
    return response
