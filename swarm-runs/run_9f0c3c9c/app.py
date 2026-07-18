from flask import Flask
from routes.checkout import checkout_bp

app = Flask(__name__)
app.register_blueprint(checkout_bp)

if __name__ == '__main__':
    app.run(debug=True)
