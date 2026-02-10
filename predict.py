import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
import os

def train_and_predict(ticker="AAPL"):
    # 1. Load the  data (Processed)

    filename = f"{ticker}_processed.csv"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run main_pipeline.py first!")
        return

    print(f"Loading data from {filename}...")
    df = pd.read_csv(filename)

    # 2. Setup Features (X) and Target (y)
    # We use the indicators we calculated earlier
    features = ["MA50", "Daily_Return", "Volatility"]
    X = df[features]
    y = df["Target"]

    # 3. Split Data (Train vs Test)
    # We train on the past (first 80%) and test on the "future" (last 20%)
    split_index = int(len(df) * 0.8)
    
    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # 4. Train the Model
    # n_estimators=100 means we create 100 "decision trees" and vote on the result
    # min_samples_split=10 prevents overfitting (memorizing the noise)
    model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
    
    print("Training Random Forest Model...")
    model.fit(X_train, y_train)

    # 5. Evaluate
    preds = model.predict(X_test)
    precision = precision_score(y_test, preds)
    print(f"Model Precision: {precision:.2f}")
    # Note: Precision > 0.5 is actually good in stock trading!
    
    # 6. Predict Tomorrow
    # We take the very last row of data (today's data) to predict tomorrow
    latest_data = X.iloc[[-1]] 
    prediction = model.predict(latest_data)
    prob = model.predict_proba(latest_data)[0][1] # Probability of "Up"

    print("\n-----------------------------")
    print(f"PREDICTION FOR {ticker} TOMORROW:")
    if prediction[0] == 1:
        print(f"BUY / UP (Confidence: {prob:.0%})")
    else:
        print(f"SELL / DOWN (Confidence: {1-prob:.0%})")
    print("-----------------------------\n")

if __name__ == "__main__":
    train_and_predict("AAPL")