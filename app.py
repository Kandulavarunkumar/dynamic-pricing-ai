from flask import Flask, render_template, request, session, redirect, jsonify
from model import predict_price
from competitor_api import get_competitor_prices
from database import get_connection
from auth import auth
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

app.register_blueprint(auth)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        product = request.form["product"]
        demand = float(request.form["demand"])

        prices = get_competitor_prices(product)
        competitor_avg = sum(prices.values()) / len(prices)

        result = predict_price(demand, competitor_avg)

        # Save to DB
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO pricing_history 
            (demand, amazon, flipkart, meesho, recommended)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            demand,
            prices["amazon"],
            prices["flipkart"],
            prices["meesho"],
            result
        ))

        conn.commit()
        cur.close()
        conn.close()

    return render_template("index.html", result=result)

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pricing_history ORDER BY created_at DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("admin.html", data=data)

@app.route("/live-data")
def live_data():
    import random
    return jsonify({"price": random.randint(1200, 1800)})

if __name__ == "__main__":
    app.run(debug=True)
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)