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
        exists = db.session.query(Tasks.name).filter_by(name=request.form["name"]).first() is not None
        if exists is False:
            task = Tasks(name=request.form["name"],
                         desc=request.form["description"],
                         status=request.form["status"] if request.form["status"] is not None else "TODO")
            db.session.add(task)
            db.session.commit()
        return "OK"


@app.route('/remove_task', methods=["POST"])
def remove_task():
    if request.method == "POST":
        exists = db.session.query(Tasks.name).filter_by(name=request.form["name"]).first() is not None
        deleted = db.session.query(Tasks.is_deleted).filter_by(name=request.form["name"]).first() is True
        if exists and not deleted:
            task = db.session.query(Tasks).filter_by(name=request.form["name"]).first()
            task.is_deleted = True
            db.session.add(task)
            db.session.commit()
            return "OK"
        elif exists and deleted:
            return "Already deleted"
        return "Not exists"


if __name__ == '__main__':
    app.run(debug=True)
