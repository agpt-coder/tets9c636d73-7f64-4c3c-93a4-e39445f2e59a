from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatedPurchaseDetails(BaseModel):
    """
    Model representing the updated purchase details.
    """

    purchaseId: int
    supplierId: int
    quantity: int


class UpdateSeedlingPurchaseResponse(BaseModel):
    """
    Response model that confirms the updates to the seedling purchase record. It includes status of the update and optionally the updated details of the seedling purchase.
    """

    success: bool
    updatedPurchaseDetails: Optional[UpdatedPurchaseDetails] = None


async def updateSeedlingPurchase(
    purchaseId: int, newSupplierId: Optional[int], newQuantity: Optional[int]
) -> UpdateSeedlingPurchaseResponse:
    """
    Updates an existing seedling purchase record. This endpoint allows modifications to purchase details such as changing supplier or adjusting quantities. Changes here will trigger adjustments in the Inventory levels.

    Args:
        purchaseId (int): The ID of the purchase record to be updated.
        newSupplierId (Optional[int]): New supplier ID in case the supplier is being changed.
        newQuantity (Optional[int]): New quantity of seedlings to adjust the purchase record and associated inventory levels.

    Returns:
        UpdateSeedlingPurchaseResponse: Response model that confirms the updates to the seedling purchase record. It includes status of the update and optionally the updated details of the seedling purchase.
    """
    if not newSupplierId and (not newQuantity):
        return UpdateSeedlingPurchaseResponse(success=False)
    existing_purchase = await prisma.models.LineItem.prisma().find_unique(
        where={"id": purchaseId}
    )
    if not existing_purchase:
        return UpdateSeedlingPurchaseResponse(success=False)
    updated_data = {}
    inventory_adjustments = []
    if newSupplierId:
        updated_data["itemId"] = newSupplierId
    if newQuantity is not None and newQuantity != existing_purchase.quantity:
        inventory_adjustments.append(
            {
                "itemId": existing_purchase.itemId,
                "eventType": "ADJUSTED",
                "quantityChange": newQuantity - existing_purchase.quantity,
            }
        )
        updated_data["quantity"] = newQuantity
    if updated_data:
        await prisma.models.LineItem.prisma().update(
            where={"id": purchaseId}, data=updated_data
        )
    for adjustment in inventory_adjustments:
        await prisma.models.InventoryEvent.prisma().create(data=adjustment)
    updated_purchase = await prisma.models.LineItem.prisma().find_unique(
        where={"id": purchaseId}
    )
    if updated_purchase:
        return UpdateSeedlingPurchaseResponse(
            success=True,
            updatedPurchaseDetails=UpdatedPurchaseDetails(
                purchaseId=updated_purchase.id,
                supplierId=updated_purchase.itemId,
                quantity=updated_purchase.quantity,
            ),
        )
    else:
        return UpdateSeedlingPurchaseResponse(success=False)
