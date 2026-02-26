from flask import Flask, render_template, request
from model import predict_price, calculate_profit, get_accuracy, generate_graph

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    profit = None
    graph = False

    if request.method == "POST":
        demand = float(request.form["demand"])
        amazon = float(request.form["amazon_price"])
        flipkart = float(request.form["flipkart_price"])
        meesho = float(request.form["meesho_price"])

        result = predict_price(demand, amazon, flipkart, meesho)
        profit = calculate_profit(result)
        generate_graph()
        graph = True

    return render_template(
        "index.html",
        result=result,
        profit=profit,
        accuracy=get_accuracy(),
        graph=graph
    )

if __name__ == "__main__":
    app.run(debug=True)