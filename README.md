# 📈 End-to-End Stock Market Prediction Pipeline

**A Full-Stack Data Engineering & Machine Learning Project**

## 🚀 Project Overview
This application is a real-time data pipeline that extracts financial market data, processes it in the cloud, and uses Machine Learning to predict future stock movements. 

It bridges the gap between **Data Engineering** (ETL, Cloud Storage) and **Data Science** (Feature Engineering, Predictive Modeling).

## 🏗️ Architecture
**`Source (Yahoo Finance API)`** 👇  
**`Extraction Script (Python)`** $\rightarrow$ *Raw Data to AWS S3 (Data Lake)* 👇  
**`Transformation Script (Pandas)`** $\rightarrow$ *Cleaned Data & Technical Indicators* 👇  
**`Machine Learning (Random Forest)`** $\rightarrow$ *Predictive Signal (Buy/Sell)* 👇  
**`Frontend (Streamlit)`** $\rightarrow$ *Interactive Dashboard for End-Users*

## ✨ Key Features
* **Live Data Extraction:** Fetches real-time OHLCV data for any S&P 500 stock.
* **Cloud-Native Storage:** Simulates a Data Lake architecture using **AWS S3** to store raw and processed datasets.
* **Technical Analysis:** Automatically calculates Moving Averages (MA50), RSI, and Volatility.
* **Machine Learning:** A Random Forest Classifier trained on historical data to predict if tomorrow's price will CLOSE HIGHER (1) or LOWER (0).
* **Interactive UI:** Built with Streamlit & Plotly for dynamic financial visualization.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Cloud:** AWS S3 (Boto3)
* **ETL:** Pandas, NumPy
* **ML:** Scikit-Learn (Random Forest)
* **Visualization:** Streamlit, Plotly
* **API:** yfinance

## ⚡ How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/LoRdElectrod/stock_prediction_app
2. Install Dependencies:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py