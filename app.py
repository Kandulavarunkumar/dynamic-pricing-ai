from flask import Flask, render_template, request
import os
from database import get_connection
from competitor_api import get_competitor_prices

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    product = request.form.get("product")
    demand = request.form.get("demand")

    if not product or not demand:
        return "Missing data", 400

    demand = float(demand)

    prices = get_competitor_prices(product)

    amazon = prices["amazon"]
    flipkart = prices["flipkart"]
    meesho = prices["meesho"]

    recommended = (amazon + flipkart + meesho) / 3 + demand * 5

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pricing_history (product, demand, amazon, flipkart, meesho, recommended) VALUES (%s,%s,%s,%s,%s,%s)",
            (product, demand, amazon, flipkart, meesho, recommended)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB ERROR:", e)

    return render_template("index.html",
                           amazon=amazon,
                           flipkart=flipkart,
                           meesho=meesho,
                           recommended=recommended)


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run()