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
        CREATE TABLE IF NOT EXISTS history(
                        id PRIMARY KEY,
                        data BLOB
        );"""
        self.db.execute(create_history_sql)

    def get_log(self, *log_id: str):
        if log_id:
            sql = F"SELECT data FROM history WHERE id = ?"
            return json.loads(self.db.execute(sql, log_id).fetchone()[0])
        else:
            sql = F"SELECT data FROM history"
            res = self.db.execute(sql).fetchall()
            return list(
                json.loads(x[0])
                for x in res)

    def add_log_entry(self, log_id: str, data: json):
        """ TODO Implement

        :param log_id:
        :param data:
        :return:
        """
        sql = """INSERT INTO history (id, data) VALUES ("das", "{"lodasl":"rofl"}")"""
        self.db.execute(sql)
        self.db.commit()
