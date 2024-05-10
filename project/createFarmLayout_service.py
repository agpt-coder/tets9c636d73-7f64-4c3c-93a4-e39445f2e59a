from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Dimensions(BaseModel):
    """
    Dimensions type detailing width and height of the farm layout.
    """

    width: float
    height: float


class Coordinate(BaseModel):
    """
    Coordinate object containing latitude and longitude for a specific area.
    """

    latitude: float
    longitude: float


class FarmLayoutResponse(BaseModel):
    """
    Response model returning the newly created farm layout with its ID included.
    """

    id: int
    name: str
    dimensions: Dimensions
    coordinates: List[Coordinate]


async def createFarmLayout(
    name: str, dimensions: Dimensions, coordinates: List[Coordinate]
) -> FarmLayoutResponse:
    """
    Allows creation of a new farm layout. Users can provide map details such as name, dimensions, and specific coordinates of areas. The server should validate the input, create a new map record in the database, and return the created object with an ID. Essential for expanding or re-configuring farm spaces.

    Args:
        name (str): The name of the farm layout.
        dimensions (Dimensions): The dimensions of the farm layout, typically width and height.
        coordinates (List[Coordinate]): List of coordinate objects, representing different areas of the farm layout.

    Returns:
        FarmLayoutResponse: Response model returning the newly created farm layout with its ID included.
    """
    layout = await prisma.models.Item.prisma().create(
        data={
            "name": name,
            "category": "EQUIPMENT",
            "stockLevel": 1,
            "minStockLevel": 1,
        }
    )
    layout_id = layout.id
    response = FarmLayoutResponse(
        id=layout_id, name=name, dimensions=dimensions, coordinates=coordinates
    )
    return response
