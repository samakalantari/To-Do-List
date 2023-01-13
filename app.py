from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# create DataBase and App
db = SQLAlchemy()
app = Flask(__name__)

# Configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ToDoList.sqlite3"
db.init_app(app)

from TODOApp.models import *

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/add_task', methods=["POST"])
def add_task():
    if request.method == "POST":
        print(request.get_data())
        task = Tasks(name=request.form["name"],
                     desc=request.form["description"],
                     status=request.form["status"])
        db.session.add(task)
        db.session.commit()
        return True



if __name__ == '__main__':
    app.run(debug=True)
