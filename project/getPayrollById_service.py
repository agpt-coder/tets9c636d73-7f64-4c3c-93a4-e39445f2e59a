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


async def getPayrollById(id: int) -> PayrollResponse:
    """
    Retrieves detailed information of a specific payroll entry by ID. This information includes all data relevant to the
    payroll calculation and status integrated with QuickBooks for updates. The expected response is a single detailed
    payroll record.

    Args:
        id (int): The unique identifier of the payroll entry to retrieve.

    Returns:
        PayrollResponse: Response model containing the updated payroll details to reflect changes made in the system.

    Example:
        payroll_record = await getPayrollById(1)
        print(payroll_record)
    """
    payroll_entry = await prisma.models.Payroll.prisma().find_unique(
        where={"id": id}, include={"user": {"include": {"profile": True}}}
    )
    if payroll_entry is None:
        raise ValueError("No payroll data found for the provided ID.")
    user_profile = (
        payroll_entry.user.profile
        if payroll_entry.user.profile
        else UserProfile(firstName="", lastName="", contactNumber=None)
    )
    payroll_response = PayrollResponse(
        id=payroll_entry.id,
        paymentAmount=payroll_entry.paymentAmount,
        taxDeductions=payroll_entry.taxDeductions,
        netAmount=payroll_entry.netAmount,
        paymentDate=payroll_entry.paymentDate,
        user=User(
            id=payroll_entry.user.id,
            email=payroll_entry.user.email,
            role=Role(role_value=payroll_entry.user.role),
            profile=user_profile,
        ),
    )
    return payroll_response
