from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class UserProfile(BaseModel):
    """
    Supplementary profile model for users containing non-authentication specific details.
    """

    lastName: str
    firstName: str
    contactNumber: Optional[str] = None


class User(BaseModel):
    """
    Model representing a user, including their roles and profile details.
    """

    id: int
    email: str
    role: Role
    profile: Optional[UserProfile] = None


class PayrollResponse(BaseModel):
    """
    Response model containing the updated payroll details to reflect changes made in the system.
    """

    id: int
    paymentAmount: float
    taxDeductions: float
    netAmount: float
    paymentDate: datetime
    user: User


async def updatePayrollEntry(
    id: int, paymentAmount: float, taxDeductions: float, netAmount: float
) -> PayrollResponse:
    """
    Updates a specific payroll entry by ID. Allows modifications to payroll details which are then reflected in QuickBooks upon syncing. The expected response is the updated payroll data confirming the changes made.

    Args:
        id (int): The unique identifier of the payroll entry to update.
        paymentAmount (float): The payment amount to be updated.
        taxDeductions (float): Updated tax deductions associated with the payroll entry.
        netAmount (float): Updated net amount after deductions.

    Returns:
        PayrollResponse: Response model containing the updated payroll details to reflect changes made in the system.

    Example:
        updated_entry = await updatePayrollEntry(1, 5000.0, 500.0, 4500.0)
        print(updated_entry)
    """
    payroll = await prisma.models.Payroll.prisma().find_unique(where={"id": id})
    if payroll is None:
        raise ValueError(f"Payroll entry with ID {id} does not exist.")
    updated_payroll = await prisma.models.Payroll.prisma().update(
        where={"id": id},
        data={
            "paymentAmount": paymentAmount,
            "taxDeductions": taxDeductions,
            "netAmount": netAmount,
            "paymentDate": datetime.now(),
        },
    )
    user_info = await prisma.models.User.prisma().find_unique(
        where={"id": updated_payroll.userId}, include={"profile": True, "role": True}
    )
    return PayrollResponse(
        id=updated_payroll.id,
        paymentAmount=updated_payroll.paymentAmount,
        taxDeductions=updated_payroll.taxDeductions,
        netAmount=updated_payroll.netAmount,
        paymentDate=updated_payroll.paymentDate,
        user=User(
            id=user_info.id,
            email=user_info.email,
            role=user_info.role,
            profile=user_info.profile,
        ),
    )
