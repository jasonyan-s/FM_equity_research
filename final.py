import yfinance as yf
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import pandas as pd
import Ratios as ratios

# Define helper functions
def calculate_dividend_yield(dividend, price):
    return dividend / price if dividend and price else 0

def calculate_eps(earnings, shares):
    return earnings / shares if earnings and shares else 0

def calculate_pe_ratio(price, eps):
    return price / eps if eps else 0

def calculate_roa(earnings, assets):
    return earnings / assets if assets else 0

def get_dcf_extract():
    dcf_file = "DCF_model.xlsx"
    if os.path.exists(dcf_file):
        df = pd.read_excel(dcf_file)
        table_content = df.head(5).to_string(index=False)
        print("\nDCF Model Table:")
        print("-" * 50)
        print(table_content)
        print("-" * 50)
        return table_content
    return ""

def get_cba_stock_info():
    try:
        ticker = "CBA.AX"
        stock = yf.Ticker(ticker)
        cba_stock_price = stock.info.get("regularMarketPrice", "N/A")
        cba_market_cap = stock.info.get("marketCap", "N/A")
        cba_eps = stock.info.get("trailingEps", "N/A")

        if cba_stock_price == "N/A":
            cba_stock_price = stock.history(period="1d")["Close"].iloc[-1]
        if cba_market_cap == "N/A":
            cba_market_cap = cba_stock_price * stock.info.get("sharesOutstanding", 0)

        return cba_stock_price, cba_market_cap, cba_eps
    except Exception as e:
        print(f"Error fetching CBA stock info: {e}")
        return "N/A", "N/A", "N/A"

def calculate_cba_eps():
    try:
        ticker = "CBA.AX"
        stock = yf.Ticker(ticker)
        cba_net_income = stock.info.get("netIncomeToCommon", "N/A")
        cba_shares_outstanding = stock.info.get("sharesOutstanding", "N/A")

        if cba_net_income != "N/A" and cba_shares_outstanding != "N/A" and cba_shares_outstanding != 0:
            return calculate_eps(cba_net_income, cba_shares_outstanding)
        else:
            return "N/A"
    except Exception as e:
        print(f"Error calculating CBA EPS: {e}")
        return "N/A"

if __name__ == "__main__":
    TICKER = input('Enter a stock ticker (e.g. BHP.AX): ').upper()

    try:
        stock = yf.Ticker(TICKER)
        stock_prices = stock.history(period="10y")
        stock_info = stock.info
        stock_financials = stock.financials
        stock_balance_sheet = stock.balance_sheet

        last_price = stock_prices['Close'].iloc[-1]
        earnings = stock_financials.loc["Net Income"].iloc[0] if "Net Income" in stock_financials.index else 0
        dividend = stock_info.get('lastDividendValue', 0)
        shares_outstanding = stock_info.get('sharesOutstanding', 0)
        total_assets = (
            stock_balance_sheet.loc["Total Assets"].iloc[0] + stock_balance_sheet.loc["Total Assets"].iloc[1]
        ) / 2 if "Total Assets" in stock_balance_sheet.index else 0

        dividend_yield = calculate_dividend_yield(dividend, last_price) * 100
        eps = calculate_eps(earnings, shares_outstanding)
        pe_ratio = calculate_pe_ratio(last_price, eps)
        roa = calculate_roa(earnings, total_assets) * 100

        chart_file = f"{TICKER}_chart.png"
        plt.figure(figsize=(10, 5))
        plt.plot(stock_prices['Close'], label="Stock Price")
        plt.title(f"{TICKER} Stock Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.savefig(chart_file)
        plt.close()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=24, style="B")
        pdf.cell(200, 20, txt=f"Equity Research Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=18)
        pdf.cell(200, 10, txt=f"Company: {TICKER}", ln=True, align="C")
        pdf.image(chart_file, x=60, y=50, w=90)
        pdf.ln(100)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Prepared by: .json Pty. Ltd.", ln=True, align="C")
        pdf.cell(200, 10, txt="Date: March 26, 2025", ln=True, align="C")

        pdf.add_page()
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="Table of Contents", ln=True, align="L")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="1. Financial Metrics", ln=True, align="L")
        pdf.cell(200, 10, txt="2. Stock Price Chart", ln=True, align="L")
        pdf.cell(200, 10, txt="3. Disclaimer", ln=True, align="L")

        pdf.add_page()
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="1. Financial Metrics", ln=True, align="L")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Last Share Price: {last_price:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"PE Ratio: {pe_ratio:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Dividend Yield: {dividend_yield:.2f}%", ln=True)
        pdf.cell(200, 10, txt=f"EPS: {eps:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"ROA: {roa:.2f}%", ln=True)

        pdf.add_page()
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="2. Stock Price Chart", ln=True, align="L")
        pdf.ln(10)
        pdf.image(chart_file, x=10, y=30, w=190)

        pdf.add_page()
        pdf.set_font("Arial", size=16, style="B")
        pdf.cell(200, 10, txt="3. Disclaimer", ln=True, align="L")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt="This report is for informational purposes only and does not constitute financial advice. "
                                     "Investors should conduct their own research or consult a financial advisor before making "
                                     "investment decisions. The data presented in this report is based on publicly available "
                                     "information and is subject to change.")

        pdf_file = f"{TICKER}_report.pdf"
        pdf.output(pdf_file)
        print(f"PDF report generated: {pdf_file}")

        if os.path.exists(chart_file):
            os.remove(chart_file)

        get_dcf_extract()

    except Exception as e:
        print(f"Error: {e}")
