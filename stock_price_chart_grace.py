import yfinance as yf
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import pandas as pd


def stock_price_chart():
    price_data = pd.read_csv("CBA.csv", parse_dates=["Date"])
    plt.figure(figsize=(6, 2))
    plt.plot(price_data['Date'], price_data['Close'])
    plt.title("CBA Historical Price")
    plt.xlabel("Date")
    plt.ylabel("Close")
    plt.tight_layout()
    chart_path = "price_chart.png"
    plt.savefig(chart_path)
    plt.close()
   