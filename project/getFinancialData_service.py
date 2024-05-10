from typing import Dict

import httpx
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class QuickBooksFinancialDataResponse(BaseModel):
    """
    Response model containing structured financial data retrieved from QuickBooks. This includes assets, liabilities, and various statements.
    """

    current_assets: float
    liabilities: float
    income_statement: Dict[str, float]
    balance_sheet: Dict[str, float]


async def get_quickbooks_financial_data(api_key: str) -> Dict[str, float]:
    """
    Utility function to fetch data from QuickBooks using the API.

    Args:
        api_key (str): The API key for authentication.

    Returns:
        Dict[str, float]: Parsed JSON data returned from QuickBooks API.

    Example:
        api_key = 'YOUR_API_KEY'
        get_quickbooks_financial_data(api_key)
        > {'current_assets': 1000.0, 'liabilities': 500.0, 'income_statements': {'revenue': 1200.0}, 'balance_sheet': {'total_assets': 1500}}
    """
    url = "https://api.quickbooks.com/getFinancialData"
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
    return resp.json()


async def getFinancialData(role: Role, api_key: str) -> QuickBooksFinancialDataResponse:
    """
    Fetches consolidated financial data from QuickBooks. This includes current financial status, transactions, and summary reports. It uses the QuickBooks API to retrieve the data securely and formats it for internal use. The response includes objects like current assets, liabilities, income statements, and balance sheets.

    Args:
    role (Role): The role of the user making the request to ensure it's a System Administrator or Financial Manager.
    api_key (str): API key used for integrating and authenticating with QuickBooks.

    Returns:
    QuickBooksFinancialDataResponse: Response model containing structured financial data retrieved from QuickBooks. This includes assets, liabilities, and various statements.

    Raises:
    ValueError: If the role is not authorized.
    """
    authorized_roles = {"SYSTEM_ADMINISTRATOR", "FINANCIAL_MANAGER"}
    if role.role_value not in authorized_roles:
        raise ValueError("Unauthorized role for this operation")
    data = await get_quickbooks_financial_data(api_key)
    return QuickBooksFinancialDataResponse(
        current_assets=data.get("current_assets", 0),
        liabilities=data.get("liabilities", 0),
        income_statement=data.get("income_statement", {}),
        balance_sheet=data.get("balance_sheet", {}),
    )
