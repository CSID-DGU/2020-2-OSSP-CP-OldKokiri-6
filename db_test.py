from db_interface import InterfDB

idb = InterfDB("score.db")

idb.init_db()
idb.query_db("insert into user(username, score) values ('nnn', '123');")
idb.db.commit()
result = idb.query_db("select * from user;")
print(result)
