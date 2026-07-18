from flask import Flask, jsonify

app = Flask(__name__)

# Mock product data
PRODUCTS = [
    {"id": 1, "name": "Widget", "price": 1999, "category": "Tools"},
    {"id": 2, "name": "Gadget", "price": 2999, "category": "Electronics"},
    {"id": 3, "name": "Doohickey", "price": 999, "category": "Accessories"}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True)
