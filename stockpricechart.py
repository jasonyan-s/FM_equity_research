import yfinance as yf
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import Ratios as ratios
import excel as e

# Define helper functions 
def calculate_dividend_yield(dividend, price):
    return dividend / price if dividend and price else 0

def calculate_eps(earnings, shares):
    return earnings / shares if earnings and shares else 0

def calculate_pe_ratio(price, eps):
    return price / eps if eps else 0

def calculate_roa(earnings, assets):
    return earnings / assets if earnings and assets else 0

# Take user input for ticker
TICKER = input('Enter a stock ticker (e.g. BHP.AX): ').upper()

try:
    # Get stock information
    stock = yf.Ticker(TICKER)
    stock_prices = stock.history(period="10y")
    stock_info = stock.info
    stock_financials = stock.financials
    stock_balance_sheet = stock.balance_sheet

    # Extract relevant information with error handling
    last_price = stock_prices['Close'].iloc[-1]
    earnings = stock_financials.loc["Net Income"].iloc[0] if "Net Income" in stock_financials.index else 0
    dividend = stock_info.get('lastDividendValue', 0)
    shares_outstanding = stock_info.get('sharesOutstanding', 0)
    total_assets = (
        stock_balance_sheet.loc["Total Assets"].iloc[0] + stock_balance_sheet.loc["Total Assets"].iloc[1]
    ) / 2 if "Total Assets" in stock_balance_sheet.index else 0

    # Calculate financial metrics
    dividend_yield = calculate_dividend_yield(dividend, last_price) * 100
    eps = calculate_eps(earnings, shares_outstanding)
    pe_ratio = calculate_pe_ratio(last_price, eps)
    roa = calculate_roa(earnings, total_assets) * 100

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

    # Generate PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover Page
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

    # Table of Contents
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Table of Contents", ln=True, align="L")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="1. Financial Metrics", ln=True, align="L")
    pdf.cell(200, 10, txt="2. Stock Price Chart", ln=True, align="L")
    pdf.cell(200, 10, txt="3. DCF Model Extract", ln=True, align="L")
    pdf.cell(200, 10, txt="4. Disclaimer", ln=True, align="L")

    # Financial Metrics Section
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

    # Stock Price Chart Section
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="2. Stock Price Chart", ln=True, align="L")
    pdf.ln(10)
    pdf.image(chart_file, x=10, y=30, w=190)

    # DCF Model Extract Section
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="3. DCF Model Extract", ln=True, align="L")
    pdf.ln(10)

    dcf_df = e.get_dcf_extract()
    if not dcf_df.empty:
        col_width = pdf.w / (len(dcf_df.columns) + 1)
        row_height = 8

        pdf.set_font("Arial", 'B', 10)
        for column in dcf_df.columns:
            pdf.cell(col_width, row_height, str(column), border=1, align='C')
        pdf.ln(row_height)
        pdf.set_font("Arial", '', 10)
        for index, row in dcf_df.iterrows():
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1)
            pdf.ln(row_height)
    else:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="DCF data not available.", ln=True, align="L")

    # Disclaimer Section
    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="4. Disclaimer", ln=True, align="L")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This report is for informational purposes only and does not constitute financial advice. "
                               "Investors should conduct their own research or consult a financial advisor before making "
                               "investment decisions. The data presented in this report is based on publicly available "
                               "information and is subject to change.")

    # Save the PDF
    pdf_file = f"{TICKER}_report.pdf"
    pdf.output(pdf_file)
    print(f"PDF report generated: {pdf_file}")

    # Clean up the chart image
    if os.path.exists(chart_file):
        os.remove(chart_file)

except Exception as e:
    print(f"Error: {e}")
