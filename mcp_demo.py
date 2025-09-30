# mcp_demo.py
import os
import sys
import logging
from datetime import datetime
import traceback

# Use a non-interactive backend so plotting works on servers / headless envs
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# --- Agent 1: Query Parser ---
def parse_query(query: str):
    """
    Improved parser:
    - Detects tickers like TSLA, AAPL, etc.
    - Maps company names (Tesla → TSLA).
    - Ignores common finance words like YTD, stock, gain.
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

    # Words we should ignore when looking for tickers
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
        raise ValueError("Couldn't detect ticker from query. Try 'TSLA' or 'Tesla' in the query.")

    # detect the intent: default to 'plot_ytd'
    intent = "plot_ytd"
    if "gain" in q or "percentage" in q or "change" in q:
        intent = "plot_ytd_and_gain"

    return {"ticker": ticker, "intent": intent}


# --- Agent 2: Code Writer (returns a callable analysis function) ---
def code_writer(structured_request):
    """
    Build a callable that, when executed, performs the data fetch, analysis and plotting.
    This emulates code generation but keeps it safe and controlled.
    """
    ticker = structured_request["ticker"]
    intent = structured_request["intent"]

    def analysis():
        logging.info(f"Fetching YTD data for {ticker}...")
        # Try a few ways to get YTD; prefer history(period="ytd")
        try:
            t = yf.Ticker(ticker)
            df = t.history(period="ytd")
            if df.empty:
                # fallback to download from start-of-year to today
                start = datetime(datetime.now().year, 1, 1).strftime("%Y-%m-%d")
                df = yf.download(ticker, start=start, progress=False)
        except Exception as e:
            raise RuntimeError(f"Error fetching data for {ticker}: {e}")

        if df is None or df.empty:
            raise RuntimeError(f"No data returned for {ticker} (empty DataFrame). Check ticker or network.")

        # Ensure Close column present
        if 'Close' not in df.columns:
            raise RuntimeError("No 'Close' column in fetched data.")

        # compute YTD gain
        first_close = df['Close'].iloc[0]
        last_close = df['Close'].iloc[-1]
        pct_gain = (last_close - first_close) / first_close * 100.0

        # create a plot
        plt.figure(figsize=(8, 4.5))
        plt.plot(df.index, df['Close'], linewidth=1.5)
        plt.title(f"YTD Close Price of {ticker} — Gain: {pct_gain:.2f}%")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        # annotate start and end
        plt.scatter([df.index[0], df.index[-1]], [first_close, last_close], zorder=5)
        plt.grid(True, linestyle="--", linewidth=0.4)

        out_path = f"{ticker}_ytd_plot.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close()

        # Prepare result
        result = {
            "ticker": ticker,
            "first_date": str(df.index[0].date()),
            "last_date": str(df.index[-1].date()),
            "first_close": float(first_close),
            "last_close": float(last_close),
            "pct_gain": float(pct_gain),
            "plot_path": out_path,
            "rows": len(df)
        }
        return result

    return analysis


# --- Agent 3: Code Executor ---
def execute(analysis_callable):
    """
    Runs the callable and returns result. Catches exceptions and returns structured errors.
    """
    try:
        res = analysis_callable()
        logging.info("Execution successful.")
        return {"success": True, "result": res}
    except Exception as err:
        tb = traceback.format_exc()
        logging.error(f"Execution failed: {err}")
        return {"success": False, "error": str(err), "traceback": tb}


# --- Small Runner to emulate the MCP host flow ---
def run_query(query: str):
    logging.info(f"Input query: {query}")

    # parse
    try:
        structured = parse_query(query)
        logging.info(f"Parsed request: {structured}")
    except Exception as e:
        return {"success": False, "stage": "parse", "error": str(e)}

    # write code (generate analysis callable)
    try:
        analysis_fn = code_writer(structured)
        logging.info("Code writer produced analysis function.")
    except Exception as e:
        return {"success": False, "stage": "code_writer", "error": str(e)}

    # execute
    exec_res = execute(analysis_fn)
    if not exec_res["success"]:
        return {"success": False, "stage": "execute", "error": exec_res["error"], "traceback": exec_res.get("traceback")}

    # success
    return {"success": True, "stage": "done", "data": exec_res["result"]}


# --- If run as script ---
if __name__ == "__main__":
    q = "Plot YTD stock gain of Tesla"
    # allow passing as CLI arg
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])

    out = run_query(q)
    if not out["success"]:
        logging.error("Flow failed at stage: %s", out.get("stage"))
        logging.error(out.get("error"))
        tb = out.get("traceback")
        if tb:
            print(tb)
        sys.exit(1)
    else:
        data = out["data"]
        logging.info("RESULT:")
        for k, v in data.items():
            logging.info(f"  {k}: {v}")
        print("\nPlot saved to:", data["plot_path"])
