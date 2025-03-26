import yfinance as yf

# Take user input for ticker
TICKER = input('Enter a stock ticker (e.g. BHP.AX): ').upper()

try:
    # Get stock information
    stock = yf.Ticker(TICKER)
    stock_prices = stock.history(period="10y")
    stock_info = stock.info
    stock_financials = stock.financials
    stock_balance_sheet = stock.balance_sheet

    # Extract relevant information
    last_price = stock_prices['Close'].iloc[-1]
    earnings = stock_financials.loc["Net Income"].iloc[0]
    dividend = stock_info['lastDividendValue']
    shares_outstanding = stock_info['sharesOutstanding']
    total_assets = (stock_balance_sheet.loc["Total Assets"].iloc[0] + stock_balance_sheet.loc["Total Assets"].iloc[1]) / 2

    dividend_yield = calculate_dividend_yield(dividend, last_price) * 100
    eps = calculate_eps(earnings, shares_outstanding)
    pe_ratio = calculate_pe_ratio(last_price, eps)
    roa = calculate_roa(earnings, total_assets) * 100

except Exception as e:
    print(f"Error: {e}")

print(f"Chosen Stock: {TICKER} \nLast Share Price: {last_price:.2f} \nPE Ratio: {pe_ratio:.2f} \nDividend Yield: {dividend_yield:.2f}% \nEPS: {eps:.2f} \nROA: {roa:.2f}%")

import matplotlib.pyplot as plt

# Plot the stock prices
plt.figure(figsize=(10, 5))
plt.plot(stock_prices['Close'])
plt.title(f"{TICKER} Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()