from flask import Flask, render_template, request, redirect, session, jsonify
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey")

# DO NOT connect to DB here at import time
from model import predict_price
from competitor_api import get_competitor_prices
from database import get_connection
from auth import auth
from flask import Flask
from database import get_connection

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devkey")

app.register_blueprint(auth)

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    profit = None
    prices = None
    try:
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pricing_history
            (demand, amazon, flipkart, meesho, recommended)
            VALUES (%s,%s,%s,%s,%s)
        """, (demand, amazon, flipkart, meesho, result))
        conn.commit()
        cur.close()
        conn.close()
except Exception as e:
    print("Database error:", e)

    if request.method == "POST":
        demand = float(request.form["demand"])
        product = request.form["product"]

        prices = get_competitor_prices(product)
        amazon = prices["amazon"]
        flipkart = prices["flipkart"]
        meesho = prices["meesho"]

        result = predict_price(demand, amazon, flipkart, meesho)
        profit = round(result - 800, 2)

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pricing_history 
                (demand, amazon, flipkart, meesho, recommended)
                VALUES (%s,%s,%s,%s,%s)
            """, (demand, amazon, flipkart, meesho, result))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("DB Error:", e)

    return render_template("index.html", result=result, profit=profit, prices=prices)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin.html")


@app.route("/live-data")
def live_data():
    import random
    return jsonify({"price": random.randint(1200, 1800)})


@app.route("/health")
def health():
    return "OK", 200
    @app.route("/")
def home():
    return "Dynamic Pricing AI Running", 200