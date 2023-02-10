from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ToDoList.sqlite3'
    instance_relative_config = True


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
