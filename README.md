# Real-Time Equity Risk Monitor 📈

A high-performance financial tracking tool designed to monitor portfolio volatility and automate risk management protocols. Built with **Python**, **SQLite**, and the **Yahoo Finance API**.

## 🚀 Overview
This system simulates an institutional-grade risk monitoring engine. It pulls real-time market data for a basket of assets (50+ tickers), calculates portfolio exposure, and triggers automated alerts based on pre-defined stop-loss thresholds (e.g., >5% intraday drop).

It is designed to demonstrate **low-latency data fetching**, **relational database persistence**, and **financial logic automation**.

## ⚡ Key Features
* **Real-Time Data Ingestion:** Fetches live OHLC (Open, High, Low, Close) data using `yfinance`.
* **Automated Risk Logic:** Continuously scans for assets breaching volatility thresholds (simulating Stop-Loss orders).
* **Data Persistence:** Utilizes **SQLite** to log trade history and alert events, ensuring data integrity (ACID properties).
* **Portfolio Health Analysis:** Calculates current P&L (Profit and Loss) relative to entry positions.

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Database:** SQLite3
* **APIs:** Yahoo Finance (`yfinance`)
* **Libraries:** Pandas (Data Manipulation), Time (Latency Management)

## ⚙️ Installation & Usage

1. **Clone the repository**
   ```bash
   git clone [https://github.com/AryanMohan818/Equity-Risk-Monitor.git](https://github.com/AryanMohan818/Equity-Risk-Monitor.git)
   cd Equity-Risk-Monitor
2. **Install Dependencies**
*   **Bash Command** = pip install yfinance pandas
3. **Run the Monitor**
*   **Bash Command** = python app.py OR    python main.py
  
📊 How It Works
1. Initialization: The script connects to the SQLite database and loads the target portfolio.

2. Polling: It queries the Yahoo Finance API at set intervals to get the current market price (CMP).

3. Risk Evaluation:

* Algorithm: Risk = (Entry_Price - Current_Price) / Entry_Price

* If Risk > 5%: The system flags the asset and logs a "CRITICAL" alert to the database.

4. Reporting: Outputs a summary of "At-Risk" assets to the console for immediate action.
