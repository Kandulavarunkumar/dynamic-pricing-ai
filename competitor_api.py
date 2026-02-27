import random

def get_competitor_prices(product_name):
    return {
        "amazon": random.randint(1200, 1700),
        "flipkart": random.randint(1250, 1750),
        "meesho": random.randint(1100, 1600)
    }