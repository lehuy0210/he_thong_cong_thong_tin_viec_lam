from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)  # Cho phép tất cả các domain (bao gồm React localhost) gọi API

app.register_blueprint(auth_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

