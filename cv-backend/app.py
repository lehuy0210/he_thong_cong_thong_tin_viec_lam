from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép tất cả các domain (bao gồm React localhost) gọi API

