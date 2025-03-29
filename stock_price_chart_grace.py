import yfinance as yf
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import ratios_james as ratios
import excel as e


def stock_price_chart(TICKER: str):
    # Get stock information
    stock = yf.Ticker(TICKER)
    stock_prices = stock.history(period="10y")
    

    # Plot the stock prices
    chart_file = f"{TICKER}_chart.png"
    plt.figure(figsize=(10, 5))
    plt.plot(stock_prices['Close'], label="Stock Price")
    plt.title(f"{TICKER} Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.savefig(chart_file)  # Save the chart as an image
    plt.close()

   

    # Clean up the chart image
    if os.path.exists(chart_file):
        os.remove(chart_file)

