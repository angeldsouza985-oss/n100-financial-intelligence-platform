import sqlite3
import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
DB = "nifty100.db"


def load_excel(file, header):
    return pd.read_excel(RAW / file, header=header)


def save_table(df, table_name, connection):

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    return len(df)


def main():

    conn = sqlite3.connect(DB)

    datasets = {

        "companies": ("companies.xlsx", 1),

        "profitandloss": ("profitandloss.xlsx", 1),

        "balancesheet": ("balancesheet.xlsx", 1),

        "cashflow": ("cashflow.xlsx", 1),

        "analysis": ("analysis.xlsx", 1),

        "documents": ("documents.xlsx", 1),

        "prosandcons": ("prosandcons.xlsx", 1),

        "sectors": ("sectors.xlsx", 0),

        "stock_prices": ("stock_prices.xlsx", 0),

        "market_cap": ("market_cap.xlsx", 0),

        "financial_ratios": ("financial_ratios.xlsx", 0),

        "peer_groups": ("peer_groups.xlsx", 0)

    }

    audit = []

    for table, (file, header) in datasets.items():

        df = load_excel(file, header)

        rows = save_table(df, table, conn)

        audit.append({

            "table_name": table,

            "rows_loaded": rows,

            "rows_rejected": 0,

            "status": "SUCCESS"

        })

        print(f"{table}: {rows}")

    pd.DataFrame(audit).to_csv(

        "output/load_audit.csv",

        index=False

    )

    conn.close()

    print("Database created.")


if __name__ == "__main__":

    main()