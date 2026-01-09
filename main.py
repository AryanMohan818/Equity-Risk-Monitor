import sqlite3
import yfinance as yf
from tabulate import tabulate
import time

# 1. SETUP DATABASE
def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    # Create a table to store your trades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            buy_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_trade(ticker, qty, price):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO portfolio (ticker, quantity, buy_price) VALUES (?, ?, ?)', 
                   (ticker.upper(), qty, price))
    conn.commit()
    conn.close()
    print(f"✅ Trade Logged: Bought {qty} of {ticker} at ${price}")

def get_portfolio():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ticker, quantity, buy_price FROM portfolio')
    data = cursor.fetchall()
    conn.close()
    return data

# 2. FETCH REAL-TIME DATA
def fetch_live_price(ticker):
    try:
        # Get data for the last 1 day to get current price
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1] # Gets the latest closing price
        else:
            return None
    except Exception as e:
        print(f"⚠️ API Error for {ticker}: {e}")
        return None

# 3. ANALYZE RISK & CALCULATE PnL
def analyze_portfolio():
    portfolio = get_portfolio() # Fetch from DB
    
    if not portfolio:
        print("Portfolio is empty.")
        return

    table_data = []
    total_invested = 0
    current_portfolio_value = 0

    print("\n🔍 FETCHING REAL-TIME DATA...")
    
    for stock in portfolio:
        ticker, qty, buy_price = stock
        
        live_price = fetch_live_price(ticker)
        
        if live_price:
            current_val = live_price * qty
            invested_val = buy_price * qty
            pnl = current_val - invested_val
            pnl_percent = (pnl / invested_val) * 100
            
            total_invested += invested_val
            current_portfolio_value += current_val

            # RISK ALERT LOGIC
            status = "🟢 SAFE"
            if pnl_percent < -5.0: # If loss is greater than 5%
                status = "🔴 CRITICAL DROP"
            elif pnl_percent < 0:
                status = "BV LOSS" # Warning

            table_data.append([ticker, qty, f"${buy_price:.2f}", f"${live_price:.2f}", 
                               f"${pnl:.2f}", f"{pnl_percent:.2f}%", status])
        else:
            table_data.append([ticker, qty, buy_price, "ERROR", "N/A", "N/A", "⚠️ NET ERROR"])

    # PRINT PROFESSIONAL TABLE
    headers = ["Ticker", "Qty", "Buy Price", "Live Price", "PnL ($)", "PnL (%)", "Risk Status"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print(f"\n💰 Total Portfolio Value: ${current_portfolio_value:.2f}")
    print(f"📉 Total PnL: ${current_portfolio_value - total_invested:.2f}")


# 4. MAIN APP LOOP
if __name__ == "__main__":
    init_db()
    
    while True:
        print("\n=== 🚀 EQUITY RISK MONITOR ===")
        print("1. Add Trade")
        print("2. View Portfolio & Risk Analysis")
        print("3. Exit")
        
        choice = input("Select Option: ")
        
        if choice == "1":
            t = input("Ticker (e.g., AAPL, GOOGL, MSFT): ")
            q = int(input("Quantity: "))
            p = float(input("Buy Price: "))
            add_trade(t, q, p)
            
        elif choice == "2":
            analyze_portfolio()
            
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid Option")


