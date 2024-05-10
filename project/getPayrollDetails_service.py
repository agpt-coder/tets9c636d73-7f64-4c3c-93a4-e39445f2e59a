from datetime import date, datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PayrollDetail(BaseModel):
    """
    Detailed information for each payroll entry.
    """

    employee_id: str
    payment_amount: float
    payment_date: datetime
    tax_deductions: float
    net_amount: float


class GetPayrollRecordsResponse(BaseModel):
    """
    Response model for a list of payroll records. Each record includes details like employee ID, payment amount, payment date, and deductions.
    """

    payrolls: List[PayrollDetail]


async def getPayrollDetails(
    employee_id: Optional[str], start_date: Optional[date], end_date: Optional[date]
) -> GetPayrollRecordsResponse:
    """
    Retrieves a list of payroll records. This endpoint uses data from the Staff Scheduling Module to ensure calculations consider current staff schedules. Each record includes details like employee id, payment amount, date, and deductions. The expected response is an array of payroll data, which integrates dynamically with QuickBooks for financial consistency.

    Args:
        employee_id (Optional[str]): Optional employee ID to filter the payroll records specifically for a given employee.
        start_date (Optional[date]): Optional start date to fetch payroll records from this date onwards.
        end_date (Optional[date]): Optional end date to fetch payroll records up to this date.

    Returns:
        GetPayrollRecordsResponse: Response model for a list of payroll records. Each record includes details like employee ID, payment amount, payment date, and deductions.

    Example:
        getPayrollDetails(employee_id="1234", start_date=date(2022, 1, 1), end_date=date(2022, 12, 31))
        > returns payroll details for employee "1234" between dates 2022-01-01 and 2022-12-31
    """
    where_query = {
        "AND": [
            {"userId": employee_id} if employee_id else None,
            {"paymentDate": {"gte": start_date}} if start_date else None,
            {"paymentDate": {"lte": end_date}} if end_date else None,
        ]
    }
    payroll_records = await prisma.models.Payroll.prisma().find_many(
        where=where_query, include={"user": True}
    )
    payroll_details = [
        PayrollDetail(
            employee_id=str(record.userId),
            payment_amount=record.paymentAmount,
            payment_date=record.paymentDate,
            tax_deductions=record.taxDeductions,
            net_amount=record.netAmount,
        )
        for record in payroll_records
        if record.user
    ]
    return GetPayrollRecordsResponse(payrolls=payroll_details)
