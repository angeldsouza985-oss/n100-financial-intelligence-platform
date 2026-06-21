def normalize_year(year):
    """
    Convert year values into a standard 4-digit format.
    """

    if year is None:
        return None

    year = str(year).strip()

    if "-" in year:
        return year.split("-")[0]

    return year


def normalize_ticker(ticker):
    """
    Convert stock ticker symbols into a standard format.
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker