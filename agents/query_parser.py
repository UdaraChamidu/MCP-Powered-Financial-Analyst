import logging

def parse_query(query: str):
    """
    Agent 1: Query Parser
    Detects ticker (TSLA, AAPL, etc.) or maps company names.
    Ignores finance words like YTD, stock, gain.
    """
    q = query.lower()
    mapping = {
        "tesla": "TSLA",
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN"
    }

    ignore_words = {"YTD", "STOCK", "GAIN", "PRICE"}

    tokens = query.replace(",", " ").split()
    ticker = None
    for t in tokens:
        if (
            t.isupper()
            and 1 <= len(t) <= 5
            and t.isalpha()
            and t not in ignore_words
        ):
            ticker = t
            break

    if not ticker:
        for name, sym in mapping.items():
            if name in q:
                ticker = sym
                break

    if not ticker:
        raise ValueError("Couldn't detect ticker from query. Try 'TSLA' or 'Tesla'.")

    intent = "plot_ytd"
    if "gain" in q or "percentage" in q or "change" in q:
        intent = "plot_ytd_and_gain"

    logging.info(f"Parsed request: ticker={ticker}, intent={intent}")
    return {"ticker": ticker, "intent": intent}
