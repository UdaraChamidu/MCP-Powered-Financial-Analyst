import logging
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

def code_writer(structured_request):
    """
    Agent 2: Code Writer
    Returns a callable analysis function to fetch data & plot.
    """
    ticker = structured_request["ticker"]
    intent = structured_request["intent"]

    def analysis():
        logging.info(f"Fetching YTD data for {ticker}...")
        try:
            t = yf.Ticker(ticker)
            df = t.history(period="ytd")
            if df.empty:
                start = datetime(datetime.now().year, 1, 1).strftime("%Y-%m-%d")
                df = yf.download(ticker, start=start, progress=False)
        except Exception as e:
            raise RuntimeError(f"Error fetching data for {ticker}: {e}")

        if df.empty:
            raise RuntimeError(f"No data returned for {ticker}.")

        first_close = df['Close'].iloc[0]
        last_close = df['Close'].iloc[-1]
        pct_gain = (last_close - first_close) / first_close * 100.0

        plt.figure(figsize=(8, 4.5))
        plt.plot(df.index, df['Close'], linewidth=1.5)
        plt.title(f"YTD Close Price of {ticker} — Gain: {pct_gain:.2f}%")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.scatter([df.index[0], df.index[-1]], [first_close, last_close], zorder=5)
        plt.grid(True, linestyle="--", linewidth=0.4)

        out_path = f"{ticker}_ytd_plot.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close()

        return {
            "ticker": ticker,
            "first_date": str(df.index[0].date()),
            "last_date": str(df.index[-1].date()),
            "first_close": float(first_close),
            "last_close": float(last_close),
            "pct_gain": float(pct_gain),
            "plot_path": out_path,
            "rows": len(df)
        }

    return analysis
