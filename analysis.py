import pandas as pd
from parser import get_metric


#YoY revenue growth
def percentage_growth(current, previous):
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None
    return ((current - previous) / previous) * 100

#Compound annual growth rate (CAGR)
def calculate_cagr(beginning, ending, years):
    if pd.isna(beginning) or pd.isna(ending) or beginning <= 0 or ending < 0 or years <= 0:
        return None
    return (((ending / beginning) ** (1 / years)) - 1) * 100

#Calculate growth rate from tables using above two functions


def calculate_growth(income_statement):
    revenue_2023 = get_metric(income_statement, "Revenue", "FY2023")
    revenue_2024 = get_metric(income_statement, "Revenue", "FY2024")
    revenue_2025 = get_metric(income_statement, "Revenue", "FY2025")
    revenue_9m_2025 = get_metric(income_statement, "Revenue", "9M2025")
    revenue_9m_2026 = get_metric(income_statement, "Revenue", "9M2026")

    FY2024_YoY = percentage_growth(revenue_2024, revenue_2023)
    FY2025_YoY = percentage_growth(revenue_2025, revenue_2024)
    YoY_9M_2026 = percentage_growth(revenue_9m_2026, revenue_9m_2025)
    FY23to25CAGR = calculate_cagr(revenue_2023, revenue_2025, 2)

    revenue_growth = {
        "FY2024_YoY": FY2024_YoY,
        "FY2025_YoY": FY2025_YoY,
        "9M2026_YoY": YoY_9M_2026,
        "FY2023_2025_CAGR": FY23to25CAGR
    }

    return {
        key: round(float(value), 2) if value is not None else None
        for key, value in revenue_growth.items()
    }




