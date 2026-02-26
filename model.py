import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import os

# Load dataset
data = pd.read_csv("data/competitor_prices.csv")

# Feature engineering
data["avg_price"] = (
    data["amazon_price"] +
    data["flipkart_price"] +
    data["meesho_price"]
) / 3

X = data[["demand", "avg_price"]]

# More realistic target
y = data["avg_price"] * (1 + (data["demand"] / 120))

# Advanced Model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Accuracy
y_pred = model.predict(X)
accuracy = r2_score(y, y_pred)

def get_accuracy():
    return round(accuracy * 100, 2)

def predict_price(demand, amazon, flipkart, meesho):
    avg_price = (amazon + flipkart + meesho) / 3
    prediction = model.predict([[demand, avg_price]])
    return round(prediction[0], 2)

def calculate_profit(price, cost=800):
    return round(price - cost, 2)

def generate_graph():
    demands = list(range(10, 101, 10))
    avg_price = 1100
    predictions = [model.predict([[d, avg_price]])[0] for d in demands]

    plt.figure()
    plt.plot(demands, predictions)
    plt.xlabel("Demand (%)")
    plt.ylabel("Predicted Price")
    plt.title("Demand vs Predicted Price")

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.savefig("static/graph.png")
    plt.close()