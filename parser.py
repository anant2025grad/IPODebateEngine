import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def clean_financial_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ["", "—", "–", "-"]:
        return None

    negative = value.startswith("(") or value.startswith("$(")

    value = (
        value.replace("$", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
    )

    try:
        number = float(value)
        return -number if negative else number
    except ValueError:
        return None


def extract_table(table, columns, periods):
    df = pd.read_html(
        StringIO(str(table)),
        flavor="lxml"
    )[0]

    df = df.iloc[4:, columns].copy()
    df.columns = ["Metric"] + periods
    df = df.dropna(subset=["Metric"])

    df["Metric"] = df["Metric"].str.strip()

    for col in periods:
        df[col] = df[col].apply(clean_financial_value)

    return df.reset_index(drop=True)


def extract_financial_statements(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")

    tables = soup.find_all("table")

    annual_periods = [
        "FY2023",
        "FY2024",
        "FY2025",
        "9M2025",
        "9M2026"
    ]

    balance_periods = [
        "FY2024",
        "FY2025",
        "Sep2026"
    ]

    income_statement = extract_table(
        tables[104],
        [0, 1, 3, 5, 7, 9],
        annual_periods
    )

    balance_sheet_part1 = extract_table(
        tables[102],
        [0, 1, 3, 5],
        balance_periods
    )

    balance_sheet_part2 = extract_table(
        tables[103],
        [0, 1, 3, 5],
        balance_periods
    )

    balance_sheet = pd.concat(
        [balance_sheet_part1, balance_sheet_part2],
        ignore_index=True
    )

    cash_flow_part1 = extract_table(
        tables[109],
        [0, 1, 3, 5, 7, 9],
        annual_periods
    )

    cash_flow_part2 = extract_table(
        tables[110],
        [0, 1, 3, 5, 7, 9],
        annual_periods
    )

    cash_flow = pd.concat(
        [cash_flow_part1, cash_flow_part2],
        ignore_index=True
    )

    return income_statement, balance_sheet, cash_flow


def get_metric(df, metric, period):
    return df.loc[df["Metric"] == metric, period].iloc[0]


def validate_balance_sheet(balance_sheet):
    results = {}

    for period in balance_sheet.columns[1:]:
        assets = get_metric(
            balance_sheet, "Total assets", period
        )

        liabilities = get_metric(
            balance_sheet, "Total liabilities", period
        )

        equity = get_metric(
            balance_sheet, "Total stockholders’ deficit", period
        )

        preferred = balance_sheet.loc[
            balance_sheet["Metric"].str.startswith(
                "Redeemable convertible preferred stock"
            ),
            period
        ].iloc[0]

        difference = assets - (liabilities + preferred + equity)

        results[period] = difference

    return results


def validate_cash_flow(cash_flow):
    results = {}

    for period in cash_flow.columns[1:]:
        operating = get_metric(
            cash_flow,
            "Net cash provided by (used in) operating activities",
            period
        )

        investing = get_metric(
            cash_flow,
            "Net cash used in investing activities",
            period
        )

        financing = get_metric(
            cash_flow,
            "Net cash provided by financing activities",
            period
        )

        fx = get_metric(
            cash_flow,
            "Effect of exchange rate changes on cash, cash equivalents, and restricted cash",
            period
        )

        reported_change = get_metric(
            cash_flow,
            "Net increase in cash, cash equivalents, and restricted cash",
            period
        )

        difference = (
            operating
            + investing
            + financing
            + (0 if pd.isna(fx) else fx)
            - reported_change
        )

        results[period] = difference

    return results
