from parser import (
    extract_financial_statements,
    validate_balance_sheet,
    validate_cash_flow
)


def main():
    file_path = "assets/Anthropic, PBC - 424(b)(4).html"

    income_statement, balance_sheet, cash_flow = (
        extract_financial_statements(file_path)
    )

    print("\n-- Consolidated Income Statement --")
    print(income_statement.to_string(index=False))

    print("\n-- Consolidated Balance Sheet --")
    print(balance_sheet.to_string(index=False))

    print("\n-- Consolidated Cash Flow Statement --")
    print(cash_flow.to_string(index=False))

    print("\n-- Balance Sheet Reconciliation --")

    for period, difference in validate_balance_sheet(
        balance_sheet
    ).items():
        print(f"{period}: {difference:,.2f}")

    print("\n-- Cash Flow Reconciliation --")

    for period, difference in validate_cash_flow(
        cash_flow
    ).items():
        print(f"{period}: {difference:,.2f}")


if __name__ == "__main__":
    main()
