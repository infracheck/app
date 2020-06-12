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
        self.db.execute('''
        CREATE TABLE IF NOT EXISTS history(
                        id PRIMARY KEY,
                        data BLOB
        );
        ''')

    def get_log(self, *log_id: str):
        if log_id:
            return json.loads(self.db.execute(F"SELECT data FROM history WHERE id = ?", log_id).fetchone()[0])
        else:
            res = self.db.execute(F"SELECT data FROM history").fetchall()
            return list(
                json.loads(x[0])
                for x in res)

    def add_log_entry(self, log_id: str, data: json):
        """ TODO Implement

        :param log_id:
        :param data:
        :return:
        """
        self.db.execute("""
        INSERT INTO history (id, data) VALUES ("das", "{"lodasl":"rofl"}")
        """)
        self.db.commit()
