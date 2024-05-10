from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CreatePayrollResponse(BaseModel):
    """
    This model provides detailed information about the newly created payroll entry, useful for confirmation and record-keeping.
    """

    payrollId: int
    userId: int
    paymentAmount: float
    paymentStatus: str


async def createPayrollEntry(
    userId: int, hoursWorked: float, hourlyWage: float, deductions: float
) -> CreatePayrollResponse:
    """
    Creates a new payroll entry. This function calculates the salary based on hours worked fetched from the Staff Scheduling Module and deductions. It integrates this data with QuickBooks to update financial records immediately. The expected response is the details of the created payroll entry, including its ID and status.

    Args:
        userId (int): Unique identifier for the employee for whom the payroll is being created.
        hoursWorked (float): Total number of hours worked by the employee in the current pay period.
        hourlyWage (float): Hourly wage rate for the employee.
        deductions (float): Any deductions from the employee's salary this period, such as taxes or benefits.

    Returns:
        CreatePayrollResponse: This model provides detailed information about the newly created payroll entry, useful for confirmation and record-keeping.
    """
    gross_payment = hoursWorked * hourlyWage
    net_payment = gross_payment - deductions
    payroll = await prisma.models.Payroll.prisma().create(
        data={
            "userId": userId,
            "paymentAmount": gross_payment,
            "taxDeductions": deductions,
            "netAmount": net_payment,
            "paymentDate": datetime.now(),
        }
    )
    response = CreatePayrollResponse(
        payrollId=payroll.id,
        userId=userId,
        paymentAmount=net_payment,
        paymentStatus="COMPLETED" if net_payment > 0 else "FAILED",
    )
    return response
