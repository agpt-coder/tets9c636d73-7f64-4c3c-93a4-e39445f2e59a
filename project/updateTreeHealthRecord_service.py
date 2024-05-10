import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateTreeHealthResponse(BaseModel):
    """
    Response model that provides feedback on the update action. It includes confirmation of the update and possibly the new state of the tree health record.
    """

    success: bool
    message: str


async def updateTreeHealthRecord(
    id: int, health_status: str, treatment_details: str
) -> UpdateTreeHealthResponse:
    """
    Updates an existing tree health record. It's used when there is a change in the health status or after a treatment has been applied. The endpoint requires tree ID and will replace the existing record with new data provided.

    Args:
      id (int): The unique identifier of the tree whose health record is to be updated.
      health_status (str): Current health status of the tree.
      treatment_details (str): Details of any treatments that have been applied to the tree.

    Returns:
      UpdateTreeHealthResponse: Response model that provides feedback on the update action. It includes confirmation of the update and possibly the new state of the tree health record.
    """
    try:
        tree_item = await prisma.models.Item.prisma().find_unique(
            where={"id": id, "category": prisma.enums.Category.TREE}
        )
        if not tree_item:
            return UpdateTreeHealthResponse(
                success=False, message=f"No tree found with ID: {id}"
            )
        updated_tree = await prisma.models.Item.prisma().update(
            where={"id": tree_item.id},
            data={
                "name": f"Tree Health Updated - {health_status}",
                "inventoryEvents": {
                    "create": [
                        {
                            "eventType": prisma.enums.InventoryEventType.ADJUSTED,
                            "quantityChange": 0,
                            "item": {"connect": {"id": tree_item.id}},
                        }
                    ]
                },
            },
        )
        return UpdateTreeHealthResponse(
            success=True, message="Tree health record updated successfully"
        )
    except Exception as e:
        return UpdateTreeHealthResponse(success=False, message=str(e))
