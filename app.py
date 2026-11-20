from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd

with open("assets/Anthropic, PBC - 424(b)(4).html", "rb") as file:
    soup = BeautifulSoup(file, "html.parser")


tables = soup.find_all("table")

for i, table in enumerate(tables, start=1):
    try:
        df = pd.read_html(StringIO(str(table)))[0]

        print(f"-- Table {i} --")
        print(df.to_string(index=False))
        print()
    except Exception as e:
        print(f"Skipping table {i}: {e}")
