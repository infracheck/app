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
        print("CREATE DATABASES")
        create_history_sql = """
        CREATE TABLE IF NOT EXISTS history(
                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      data BLOB
        );"""
        self.db.execute(create_history_sql)

    def get_log(self, limit: int = 10, offset: int = 0):
        res = self.db.execute(
            """SELECT data
            FROM history
            LIMIT ? OFFSET ?
            """, (limit, offset,)).fetchall()
        return list(
            json.loads(x[0])
            for x in res)

    def insert_test_result(self, result):
        """ TODO Implement

        :param result:
        :return:
        """
        self.db.execute("INSERT INTO history (data) VALUES (?)", (json.dumps(result),))
        self.db.commit()
