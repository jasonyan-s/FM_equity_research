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

# Function to fetch live CBA stock price, market cap, and EPS
def stock_financials(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info


    # Fetch the most recent stock price and market cap
    price = info.get("regularMarketPrice")
    market_cap = info.get("marketCap", "N/A")

    # Reported EPS
    eps_reported = info.get("trailingEps")

    # P/E Ratio
    pe_ratio = calculate_pe_ratio(price, eps_reported) if price and eps_reported else "N/A"

    # Calculated EPS
    net_income = info.get("netIncomeToCommon")
    shares_outstanding = info.get("sharesOutstanding")
    eps_calculated = calculate_eps(net_income, shares_outstanding) if net_income and shares_outstanding else "N/A"

    # Dividend Yield
    dividend = info.get("dividendRate", 0)
    dividend_yield = calculate_dividend_yield(dividend, price) if price else "N/A"

   

    return {
        "Stock Price": f"${price:,.2f}" if price else "N/A",
        "Market Cap": f"${market_cap:,.2f}" if market_cap else "N/A",
        "Reported EPS": f"{eps_reported:,.2f}" if eps_reported else "N/A",
        "Calculated EPS": f"{eps_calculated:,.2f}" if eps_calculated != "N/A" else "N/A",
        "P/E Ratio": f"{pe_ratio:,.2f}" if pe_ratio != "N/A" else "N/A",
        "Dividend Yield": f"{dividend_yield * 100:.2f}%" if dividend_yield != "N/A" else "N/A",
    }

   

