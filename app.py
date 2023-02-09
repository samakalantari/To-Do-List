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


@app.route('/task', methods=["POST"])
def add_task():
    if not request.form.get("name"):
        return {"error": "task must have name"}

    exists = db.session.query(Tasks.id).filter_by(name=request.form["name"]).first() is not None
    if not exists:
        task = Tasks(name=request.form.get("name"),
                     desc=request.form.get("description"),
                     status=request.form.get("status", "TODO"))
        if task.status is "":
            task.status = "TODO"
        db.session.add(task)
        db.session.commit()
        return {"task saved successfully": task.name}

    return {"error": "task already exists"}


@app.route('/task', methods=["DELETE"])
def remove_task():
    if not request.form.get("name"):
        return {"error": "which one?"}

    exists = db.session.query(Tasks.id).filter_by(name=request.form["name"]).first() is not None
    deleted = db.session.query(Tasks).filter_by(name=request.form["name"]).first().is_deleted is True

    if exists and not deleted:
        task = db.session.query(Tasks).filter_by(name=request.form["name"]).first()
        task.is_deleted = True
        db.session.add(task)
        db.session.commit()
        return {"task deleted successfully": task.name}
    elif exists and deleted:
        return {"task already deleted": request.form.get("name")}
    return {"error": "task {} not found".format(request.form.get("name"))}


@app.route('/tasks', methods=["GET"])
def all_tasks():
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

    return {"error": "Not exists"} if None else tasks


@app.route('/task', methods=["PUT"])
def edit_task():
    if not request.form.get("name"):
        return {"error": "which one?"}

    exists = db.session.query(Tasks.id).filter_by(name=request.form["name"]).first() is not None
    deleted = db.session.query(Tasks).filter_by(name=request.form["name"]).first().is_deleted is True

    if deleted:
        return {"error": "deleted"}

    if exists:
        task = db.session.query(Tasks).filter_by(name=request.form["name"]).first()

        task.name = request.form.get("name", task.name)
        task.status = request.form.get("status", task.status)
        task.desc = request.form.get("description", task.desc)

        db.session.add(task)
        db.session.commit()

        return {"task edited successfully": task.name}
    else:
        return {"error": "task not found"}


if __name__ == '__main__':
    app.run(debug=True)
