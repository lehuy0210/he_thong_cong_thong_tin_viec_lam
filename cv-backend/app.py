from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from flask_migrate import Migrate
import db
from routes.job_management import job_bp
from routes.cv import cv_bp
from routes.job_apply import job_apply_bp
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lehuy0210@localhost:3306/hethongcv'
db.init_app(app)
migrate = Migrate(app, db)
import models


CORS(app)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(job_bp, url_prefix='/api')
app.register_blueprint(cv_bp, url_prefix='/api')
app.register_blueprint(job_apply_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

