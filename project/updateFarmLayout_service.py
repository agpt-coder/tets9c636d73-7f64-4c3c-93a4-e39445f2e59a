from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Dimensions(BaseModel):
    """
    Dimensions type detailing width and height of the farm layout.
    """

    width: float
    height: float


class UpdateFarmLayoutResponse(BaseModel):
    """
    Confirms the successful update of a farm layout, potentially returning some information about the updated layout.
    """

    success: bool
    layoutId: str
    updatedFields: List[str]


async def updateFarmLayout(
    layoutId: str,
    mapName: Optional[str] = None,
    dimensions: Optional[Dimensions] = None,
) -> UpdateFarmLayoutResponse:
    """
    Updates an existing farm layout based on the provided layout ID. This endpoint should accept partial or full updates to fields like map name or dimensions. The system should validate changes, apply them to the specified layout, and reflect these changes in all linked modules.

    Args:
        layoutId (str): The unique identifier for the farm layout that needs updating.
        mapName (Optional[str]): The new name for the farm layout map, if provided.
        dimensions (Optional[Dimensions]): Updates to the dimensions of the farm layout map, if provided.

    Returns:
        UpdateFarmLayoutResponse: Confirms the successful update of a farm layout, potentially returning some information about the updated layout.

    Raises:
        ValueError: If the layout ID is not found in the database.
    """
    layout = await prisma.models.Item.prisma().find_unique(where={"id": int(layoutId)})
    if not layout:
        raise ValueError(f"No layout found with ID: {layoutId}")
    data_to_update = {}
    updated_fields = []
    if mapName:
        data_to_update["name"] = mapName
        updated_fields.append("name")
    if dimensions:
        data_to_update[
            "description"
        ] = f"Width: {dimensions.width}, Height: {dimensions.height}"
        updated_fields.extend(["description"])
    if data_to_update:
        await prisma.models.Item.prisma().update(
            where={"id": int(layoutId)}, data=data_to_update
        )
    return UpdateFarmLayoutResponse(
        success=True, layoutId=layoutId, updatedFields=updated_fields
    )
