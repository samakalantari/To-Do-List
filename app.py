from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create DataBase and App
db = SQLAlchemy()
app = Flask(__name__)

# Configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ToDoList.sqlite3"
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


from TODOApp.models import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
