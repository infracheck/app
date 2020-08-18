import json
import sqlite3

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
    db = sqlite3.connect('infracheck.db', check_same_thread=False)
    cursor = db.cursor()

    def __init__(self) -> None:
        create_history_sql = """
        CREATE TABLE IF NOT EXISTS history
            (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT      NOT NULL,
                description TEXT      NOT NULL,
                succeeded   INTEGER   NOT NULL,
                failures    INTEGER   NOT NULL,
                errors      INTEGER   NOT NULL,
                total       INTEGER   NOT NULL,
                plugin_data BLOB,
                message     TEXT DEFAULT 'No response message',
                datestamp   TIMESTAMP NOT NULL
            );"""
        create_presets_sql = """
        CREATE TABLE IF NOT EXISTS preset
        (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT NOT NULL,
            plugins     BLOB,
            date        DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        self.cursor.execute(create_history_sql)
        self.cursor.execute(create_presets_sql)

    def get_log(self, limit: int = 10, offset: int = 0):
        conn = self.db
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute("""
        SELECT * 
        FROM history
        ORDER BY id DESC
        LIMIT ? 
        OFFSET ?
        """, (limit, offset,)).fetchall()
        result = [dict(row) for row in rows]
        for row in result:
            row['plugin_data'] = json.loads(row['plugin_data'])
        return result

    def get_presets(self, limit: int = 10, offset: int = 0):
        conn = self.db
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute("""
        SELECT * 
        FROM preset
        ORDER BY id DESC
        LIMIT ? 
        OFFSET ?
        """, (limit, offset,)).fetchall()
        result = [dict(row) for row in rows]
        for row in result:
            row['plugin_data'] = json.loads(row['data'])
        return result

    def insert_test_result(self, result: ITestResult):
        """ Insert the test result and send back a date string
        :param result:
        :return:
        """
        self.cursor.execute(
            """INSERT INTO history (name, description, succeeded, failures, errors, total, plugin_data, message, datestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                result['name'],
                result['description'],
                result['succeeded'],
                result['failures'],
                result['errors'],
                result['total'],
                json.dumps(result['plugin_data']),
                result['message'],
                result['date']
                ,))
        self.db.commit()

    def insert_preset(self, preset):
        """ TODO Implement

        :param preset:
        :return:
        """
        self.db.execute(
            """INSERT INTO preset (name, description, plugins)
            VALUES (?, ?, ?)""", (
                preset['name'],
                preset['description'],
                json.dumps(preset['plugins'])
                ,))
        self.db.commit()
