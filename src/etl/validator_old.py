import pandas as pd
from pathlib import Path

RAW = Path("data/raw")


def validate():

    failures = []

    companies = pd.read_excel(
        RAW / "companies.xlsx",
        header=1
    )

    pnl = pd.read_excel(
        RAW / "profitandloss.xlsx",
        header=1
    )

    bs = pd.read_excel(
        RAW / "balancesheet.xlsx",
        header=1
    )

    cf = pd.read_excel(
        RAW / "cashflow.xlsx",
        header=1
    )

    # DQ-01 PK uniqueness

    duplicate_companies = companies[
        companies["id"].duplicated()
    ]

    for _, row in duplicate_companies.iterrows():

        failures.append({

            "rule_id": "DQ-01",

            "severity": "CRITICAL",

            "table": "companies",

            "company_id": row["id"],

            "message": "Duplicate company id"

        })

    # DQ-02 company_id + year uniqueness

    duplicate_years = pnl[
        pnl.duplicated(
            subset=["company_id", "year"]
        )
    ]

    for _, row in duplicate_years.iterrows():

        failures.append({

            "rule_id": "DQ-02",

            "severity": "CRITICAL",

            "table": "profitandloss",

            "company_id": row["company_id"],

            "message": "Duplicate company-year"

        })

    return pd.DataFrame(failures)


if __name__ == "__main__":

    df = validate()

    df.to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("Validation complete")