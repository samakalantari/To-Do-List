import datetime
import enum
from flask_sqlalchemy import SQLAlchemy

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DATETIME(timezone=True), default=datetime.datetime.now())
    last_modify = db.Column(db.DATETIME(timezone=True), onupdate=datetime.datetime.now())
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)


class StatusChoices(enum.Enum):
    TODO = "To-Do"
    DOING = "Doing"
    DONE = "Done"


class Tasks(BaseModel):
    __tablename__ = "tasks"

    name = db.Column(db.String(50), name="Task_name", unique=True)
    desc = db.Column(db.Text)

    status = db.Column(db.Enum(StatusChoices), default=StatusChoices.TODO)


class Tags(BaseModel):
    __tablename__ = "tags"

    name = db.Column(db.String(50))
