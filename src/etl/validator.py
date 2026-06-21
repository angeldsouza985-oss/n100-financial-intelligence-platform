import pandas as pd

RAW = "data/raw/"


def validate():

    failures = []

    # -----------------------------
    # Load files
    # -----------------------------

    companies = pd.read_excel(
        RAW + "companies.xlsx",
        header=1
    )

    pnl = pd.read_excel(
        RAW + "profitandloss.xlsx",
        header=1
    )

    balancesheet = pd.read_excel(
        RAW + "balancesheet.xlsx",
        header=1
    )

    # -----------------------------
    # Clean company ids
    # -----------------------------

    companies["id"] = (
        companies["id"]
        .astype(str)
        .str.strip()
    )

    pnl["company_id"] = (
        pnl["company_id"]
        .astype(str)
        .str.strip()
    )

    pnl["year"] = (
        pnl["year"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------
    # Numeric conversions
    # -----------------------------

    pnl["sales"] = pd.to_numeric(
        pnl["sales"],
        errors="coerce"
    )

    pnl["opm_percentage"] = pd.to_numeric(
        pnl["opm_percentage"],
        errors="coerce"
    )

    balancesheet["borrowings"] = pd.to_numeric(
        balancesheet["borrowings"],
        errors="coerce"
    )

    # -----------------------------
    # DQ-01 Duplicate company ids
    # -----------------------------

    duplicates = companies[
        companies["id"].duplicated(
            keep=False
        )
    ]

    if len(duplicates):

        failures.append({
            "rule_id": "DQ-01",
            "severity": "CRITICAL",
            "message": "Duplicate ids found"
        })

    # -----------------------------
    # DQ-02 Duplicate company-year
    # -----------------------------

    duplicate_company_year = pnl[
        pnl.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    if len(duplicate_company_year):

        failures.append({
            "rule_id": "DQ-02",
            "severity": "CRITICAL",
            "message": "Duplicate company-year"
        })

    # -----------------------------
    # DQ-03 Invalid company ids
    # -----------------------------

    invalid = pnl[
        ~pnl["company_id"].isin(
            companies["id"]
        )
    ]

    if len(invalid):

        failures.append({
            "rule_id": "DQ-03",
            "severity": "WARNING",
            "message":
            f"{len(invalid['company_id'].drop_duplicates())} invalid company ids found"
        })

    return pd.DataFrame(failures)


if __name__ == "__main__":

    df = validate()

    df.to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print(df)

    print("Validation completed.")