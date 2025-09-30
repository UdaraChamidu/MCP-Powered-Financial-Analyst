import yfinance as yf
import matplotlib.pyplot as plt

def plot_ytd_stock(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="ytd")
    df['Close'].plot(title=f"YTD Stock Price of {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.savefig("plot.png")
    return "plot.png"

