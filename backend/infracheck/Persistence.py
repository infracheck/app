import datetime
import json
from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from infracheck import db, app
from infracheck.model.ITestResult import ITestResult


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Persistence:
    """
    This class deals as wrapper for the SQLAlchemy interface
    Changes to the database model should be made here.
    """

    def __init__(self) -> None:
        self.db = SQLAlchemy(app)
        db.create_all()

    @dataclass
    class Result(db.Model):
        """
        ORM of the Result. It contains table definitions.
        If the table does not exist, it will be created when the application starts.
        """
        id: str = db.Column(db.String, primary_key=True)
        name: str = db.Column(db.String(80), nullable=False)
        description: str = db.Column(db.String(120), nullable=False)
        success_count: int = db.Column(db.String(120), nullable=False)
        failure_count: int = db.Column(db.String(120), nullable=False)
        error_count: int = db.Column(db.Integer, nullable=False)
        total_count: int = db.Column(db.Integer, nullable=False)
        plugin_result: json = db.Column(db.JSON)
        message: str = db.Column(db.String(80), nullable=False)
        date: datetime = db.Column(db.DateTime, server_default=func.now())

    def add_result(self, result: ITestResult):
        """
        Adds a rest result to the database
        :param result:
        :return:
        """
        db.session.add(self.Result(
            id=result['id'],
            name=result['name'],
            description=result['description'],
            success_count=result['success_count'],
            failure_count=result['failure_count'],
            error_count=result['error_count'],
            total_count=result['total_count'],
            plugin_result=result['plugin_result'],
            message=result['message'],
            date=result['date']
        ))
        db.session.commit()
