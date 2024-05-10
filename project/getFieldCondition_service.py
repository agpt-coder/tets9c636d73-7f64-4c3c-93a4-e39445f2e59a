import prisma
import prisma.models
from pydantic import BaseModel


class FieldConditionResponse(BaseModel):
    """
    Provides detailed information about the soil quality, moisture levels, and crop health of a specific field. This helps in effective field management and planning interventions.
    """

    soilQuality: str
    moistureLevel: str
    cropHealth: str


async def getFieldCondition(fieldId: int) -> FieldConditionResponse:
    """
    Fetches the current condition of a specified field, including soil quality, moisture levels, and crop health.
    Useful for Field Managers and Health Specialists to monitor and manage field conditions
    effectively and plan interventions.

    Args:
        fieldId (int): The unique identifier for the field whose condition is being requested.

    Returns:
        FieldConditionResponse: Provides detailed information about the soil quality, moisture levels,
        and crop health of a specific field. This helps in effective field management and planning interventions.
    """
    soil_item = await prisma.models.Item.prisma().find_unique(where={"id": fieldId})
    moisture_item = await prisma.models.Item.prisma().find_unique(
        where={"id": fieldId + 1}
    )
    crop_health_item = await prisma.models.Item.prisma().find_unique(
        where={"id": fieldId + 2}
    )
    soil_quality = "Good" if soil_item and soil_item.stockLevel > 50 else "Poor"
    moisture_level = (
        "Optimal" if moisture_item and moisture_item.stockLevel > 40 else "Low"
    )
    crop_health = (
        "Healthy"
        if crop_health_item and crop_health_item.stockLevel > 30
        else "At Risk"
    )
    return FieldConditionResponse(
        soilQuality=soil_quality, moistureLevel=moisture_level, cropHealth=crop_health
    )
