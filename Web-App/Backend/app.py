from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes_blueprints import register_blueprints
import os
from config import engine

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = f"{os.getenv('JWT_SECRET_KEY')}"

jwt = JWTManager(app)
CORS(app)

register_blueprints(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)