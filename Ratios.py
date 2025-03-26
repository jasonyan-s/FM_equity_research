import yfinance as yf

# Function to calculate the P/E ratio of a stock
def calculate_pe_ratio(price, earnings):
    return price / earnings if earnings != 0 else "N/A"

# Function to calculate the dividend yield of a stock
def calculate_dividend_yield(dividend, price):
    return dividend / price

# Function to calculate the earnings per share of a stock
def calculate_eps(price, earnings):
    return price / earnings if earnings != 0 else "N/A"

# Function to calculate ROA of a stock
def calculate_roa(net_income, total_assets):
    return net_income / total_assets

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

# Function to calculate EPS by dividing stock price by earnings
def calculate_cba_eps():
    try:
        ticker = "CBA.AX"
        stock = yf.Ticker(ticker)

        # Fetch stock price and earnings
        cba_stock_price = stock.info.get("regularMarketPrice", "N/A")
        cba_earnings = stock.info.get("totalRevenue", "N/A")  # Example: Replace with actual earnings field

        if cba_stock_price != "N/A" and cba_earnings != "N/A" and cba_earnings != 0:
            return calculate_eps(cba_stock_price, cba_earnings)
        else:
            return "N/A"
    except Exception as e:
        print(f"Error calculating CBA EPS: {e}")
        return "N/A"

# Example usage
if __name__ == "__main__":
    cba_price, cba_market_cap, cba_eps = get_cba_stock_info()
    print(f"CBA Stock Price: ${cba_price}")
    print(f"CBA Market Cap: ${cba_market_cap}")
    print(f"CBA EPS (from yfinance): {cba_eps}")

    # Calculate and print the P/E ratio
    if cba_price != "N/A" and cba_eps != "N/A":
        pe_ratio = calculate_pe_ratio(cba_price, cba_eps)
        print(f"CBA P/E Ratio: {pe_ratio}")
    else:
        print("Unable to calculate P/E Ratio due to missing data.")

    # Calculate and print EPS by dividing stock price by earnings
    cba_calculated_eps = calculate_cba_eps()
    print(f"CBA Calculated EPS: {cba_calculated_eps}")