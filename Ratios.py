import yfinance as yf

# Function to calculate the P/E ratio of a stock
def calculate_pe_ratio(price, earnings):
    return price / earnings if earnings != 0 else "N/A"

# Function to calculate the dividend yield of a stock
def calculate_dividend_yield(dividend, price):
    return dividend / price if price != 0 else "N/A"

# Function to calculate the earnings per share of a stock
def calculate_eps(net_income, shares_outstanding):
    return net_income / shares_outstanding if shares_outstanding != 0 else "N/A"

# Function to calculate ROA of a stock
def calculate_roa(net_income, total_assets):
    return net_income / total_assets if total_assets != 0 else "N/A"

# Function to fetch live CBA stock price, market cap, and EPS
def get_cba_stock_info():
    try:
        ticker = "CBA.AX"  # Ticker symbol for Commonwealth Bank of Australia on ASX
        stock = yf.Ticker(ticker)

        # Fetch the most recent stock price and market cap
        cba_stock_price = stock.info.get("regularMarketPrice", "N/A")
        cba_market_cap = stock.info.get("marketCap", "N/A")

        # Fetch EPS from stock.info
        cba_eps = stock.info.get("trailingEps", "N/A")

        # Fallback to ensure no "N/A" values
        if cba_stock_price == "N/A":
            cba_stock_price = stock.history(period="1d")["Close"].iloc[-1]
        if cba_market_cap == "N/A":
            cba_market_cap = cba_stock_price * stock.info.get("sharesOutstanding", 0)

        return cba_stock_price, cba_market_cap, cba_eps
    except Exception as e:
        print(f"Error fetching CBA stock info: {e}")
        return "N/A", "N/A", "N/A"

# Function to calculate EPS by dividing net income by shares outstanding
def calculate_cba_eps():
    try:
        ticker = "CBA.AX"
        stock = yf.Ticker(ticker)

        # Fetch net income and shares outstanding
        cba_net_income = stock.info.get("netIncomeToCommon", "N/A")  # Net income
        cba_shares_outstanding = stock.info.get("sharesOutstanding", "N/A")  # Shares outstanding

        if cba_net_income != "N/A" and cba_shares_outstanding != "N/A" and cba_shares_outstanding != 0:
            return calculate_eps(cba_net_income, cba_shares_outstanding)
        else:
            return "N/A"
    except Exception as e:
        print(f"Error calculating CBA EPS: {e}")
        return "N/A"

# Example usage
if __name__ == "__main__":
    cba_price, cba_market_cap, cba_eps = get_cba_stock_info()

    # Format and print stock price and market cap
    if cba_price != "N/A":
        cba_price = f"{cba_price:,.2f}"
    if cba_market_cap != "N/A":
        cba_market_cap = f"{cba_market_cap:,.2f}"

    print(f"CBA Stock Price: ${cba_price}")
    print(f"CBA Market Cap: ${cba_market_cap}")

    # Calculate and print the P/E ratio
    if cba_price != "N/A" and cba_eps != "N/A":
        pe_ratio = calculate_pe_ratio(float(cba_price.replace(',', '')), cba_eps)
        print(f"CBA P/E Ratio: {pe_ratio:,.2f}")
    else:
        print("Unable to calculate P/E Ratio due to missing data.")

    # Calculate and print EPS by dividing net income by shares outstanding
    cba_calculated_eps = calculate_cba_eps()
    if cba_calculated_eps != "N/A":
        print(f"CBA Calculated EPS: {float(cba_calculated_eps):,.2f}")
    else:
        print("CBA Calculated EPS: N/A")

    # Calculate and print the dividend yield
    dividend = 4.50  # Example dividend value
    if cba_price != "N/A":
        dividend_yield = calculate_dividend_yield(dividend, float(cba_price.replace(',', '')))
        print(f"CBA Dividend Yield: {dividend_yield * 100:.2f}%")
    else:
        print("Unable to calculate Dividend Yield due to missing data.")

    # Calculate and print ROA
    total_assets = 1_000_000_000_000  # Example total assets value
    cba_net_income = 10_000_000_000  # Example net income value
    roa = calculate_roa(cba_net_income, total_assets)
    print(f"CBA ROA: {roa * 100:.2f}%")