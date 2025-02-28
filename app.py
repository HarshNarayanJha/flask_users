import os

from dotenv import load_dotenv
from flask import Flask
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

app = Flask(__name__)
mongo_client = MongoClient(MONGODB_URI)

print(mongo_client)
for db_info in mongo_client.list_database_names():
    print(db_info)

@app.route("/")
def home():
    return "Hello World!!!"


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
