from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import json
import pandas as pd

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
        if not request.form.get("name"):
            return {"error": "task must have name"}

        exists = db.session.query(Tasks.name).filter_by(name=request.form["name"]).first() is not None
        if not exists:
            task = Tasks(name=request.form.get("name"),
                         desc=request.form.get("description"),
                         status=request.form.get("status", "TODO"))
            db.session.add(task)
            db.session.commit()
            return {"task saved successfully": task.name}
    return {"error": "task already exists"}



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


@app.route('/all_tasks', methods=["POST"])
def all_tasks():
    if request.method == "POST":
        data = db.session.query(Tasks).all()
        tasks = pd.DataFrame()
        for row in data:
            task = {
                "name": row.name,
                "description": row.desc,
                "status": row.status.value
            }
            tasks = tasks.append(task, ignore_index=True)
        tasks = tasks.to_json(orient="split")

    return tasks if not None else "Not exists"


if __name__ == '__main__':
    app.run(debug=True)
