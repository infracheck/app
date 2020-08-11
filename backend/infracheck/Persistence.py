import json
import sqlite3


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

    def __init__(self) -> None:
        create_history_sql = """
        CREATE TABLE IF NOT EXISTS history
        (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            description TEXT    NOT NULL,
            succeeded   INTEGER NOT NULL,
            failures    INTEGER NOT NULL,
            errors      INTEGER NOT NULL,
            total       INTEGER NOT NULL,
            data        BLOB,
            message     TEXT     DEFAULT 'No response message',
            date        DATETIME DEFAULT CURRENT_TIMESTAMP
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
        self.db.execute(create_history_sql)
        self.db.execute(create_presets_sql)

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
            row['data'] = json.loads(row['data'])
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
            row['data'] = json.loads(row['data'])
        return result

    def insert_test_result(self, result):
        """ TODO Implement

        :param result:
        :return:
        """
        self.db.execute(
            """INSERT INTO history (name, description, succeeded, failures, errors, total, data, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
                result['name'],
                result['description'],
                result['succeeded'],
                result['failures'],
                result['errors'],
                result['total'],
                json.dumps(result['data']),
                result['message']
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
