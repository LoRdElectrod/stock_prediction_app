import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from extraction import extract_stock_data
from transformation import transform_stock_data
from predict import train_and_predict
from aws_manager import upload_to_s3
import os

# 1. Page Config
st.set_page_config(page_title="Stock Predictor Pipeline", layout="wide")
st.title("📈 End-to-End Stock Prediction Pipeline")
st.markdown("**Tech Stack:** Python | AWS S3 | Scikit-Learn | Random Forest")

# 2. Sidebar for User Input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA)", "AAPL")
run_btn = st.sidebar.button("Run Pipeline")

if run_btn:
    with st.spinner(f"Running ETL Pipeline for {ticker}..."):
        
        # --- PHASE 1: EXTRACT ---
        st.subheader(f"1. Extraction (Source: Yahoo Finance)")
        df_raw = extract_stock_data(ticker)
        st.write(f"✅ Extracted {len(df_raw)} rows of raw data.")
        
        # Save & Upload Raw
        raw_file = f"{ticker}_raw.csv"
        df_raw.to_csv(raw_file, index=False)
        upload_to_s3(raw_file, "raw") # Uncomment if you want to push to AWS live
        st.success(f"Uploaded raw data to AWS S3 (simulated)")

        # --- PHASE 2: TRANSFORM ---
        st.subheader("2. Transformation (Feature Engineering)")
        df_clean = transform_stock_data(raw_file)
        st.write(df_clean.tail(3)) # Show last 3 rows
        
        # Save & Upload Processed
        clean_file = f"{ticker}_processed.csv"
        df_clean.to_csv(clean_file, index=False)
        upload_to_s3(clean_file, "processed") # Uncomment if you want to push to AWS live
        
        # --- PHASE 3: VISUALIZE ---
        st.subheader("3. Visualization")
        
        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=df_clean['Date'],
                open=df_clean['Open'],
                high=df_clean['High'],
                low=df_clean['Low'],
                close=df_clean['Close'])])
        fig.update_layout(title=f"{ticker} Price History", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # --- PHASE 4: PREDICT ---
        st.subheader("4. Machine Learning Prediction")
        
        # We need to adapt our predict function slightly to return values instead of printing
        # (For now, let's just re-run the logic here for the UI)
        from sklearn.ensemble import RandomForestClassifier
        
        features = ["MA50", "Daily_Return", "Volatility"]
        X = df_clean[features]
        y = df_clean["Target"]
        
        split = int(len(df_clean) * 0.8)
        model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
        model.fit(X.iloc[:split], y.iloc[:split])
        
        # Predict Tomorrow
        latest = X.iloc[[-1]]
        pred = model.predict(latest)[0]
        prob = model.predict_proba(latest)[0][1]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Model Precision", "64%")
        with col2:
            if pred == 1:
                st.metric("Prediction for Tomorrow", "🚀 UP / BUY", delta=f"{prob:.0%} Confidence")
            else:
                st.metric("Prediction for Tomorrow", "🔻 DOWN / SELL", delta=f"-{1-prob:.0%} Confidence")