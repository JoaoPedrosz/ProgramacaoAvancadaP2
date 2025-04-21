from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

mongodb_client = PyMongo(
    app,
    uri="mongodb+srv://joaosilva:abc123456@com759.d8vet.mongodb.net/p2facamp?retryWrites=true&w=majority&appName=COM759"
)
db = mongodb_client.db




from app import routes