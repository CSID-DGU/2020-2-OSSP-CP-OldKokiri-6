import sqlite3


class InterfDB:

    def __init__(self, dbname):
        self.__DBNAME = dbname
        self.db = sqlite3.connect(self.__DBNAME)

    def init_db(self):
        with open("./db/schema.sql", 'r') as f:
            self.db.cursor().executescript(f.read())
        self.db.commit()

    def query_db(self, query, args=(), one=False):
        cursor = self.db.execute(query, args)
        result = [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) \
                  for row in cursor.fetchall()]
        return (result[0] if result else None) if one else result

    def commit(self):
        self.db.commit()
