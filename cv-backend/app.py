from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp

from routes.job_management import job_bp
from routes.cv import cv_bp

app = Flask(__name__)
CORS(app)  # Cho phép tất cả các domain (bao gồm React localhost) gọi API

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(job_bp, url_prefix='/api')
app.register_blueprint(cv_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

