from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd

with open("assets/Anthropic, PBC - 424(b)(4).html", "rb") as file:
    soup = BeautifulSoup(file, "html.parser")


tables = soup.find_all("table")
target_index = 104
"""
for i, table in enumerate(tables, start=1):

    try:
            df = pd.read_html(StringIO(str(table)), flavor="lxml")[0]

            print(f"-- Table {i} --")
            print(df.head(2).to_string(index=False))
            print()
    except Exception as e:
        print(f"Skipping table {i}: {e}")
"""
df = pd.read_html(StringIO(str(tables[target_index])), flavor='lxml')[0]
df = df.iloc[4:].copy()
df = df.iloc[:, [0, 1, 3, 5, 7, 9]]
df.columns = [
    "Metric",
    "FY2023",
    "FY2024",
    "FY2025",
    "9M2025",
    "9M2026"
]
df.dropna(axis=0, how='all')

def clean_financial_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ["", "—", "–", "-"]:
        return None
    negative = "(" in value and ")" in value

    value = value.replace("$", "")
    value = value.replace(",", "")
    value = value.replace("(", "")
    value = value.replace(")", "")

    try:
        number = float(value)
        return -number if negative else number
    except ValueError:
        return None

financial_columns = df.columns[1:]

for col in financial_columns:
    df[col] = df[col].apply(clean_financial_value)
print()
print(f"-- Table {target_index + 1} --")
print(df.to_string(index=False))