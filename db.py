import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect("score.db")
        self.cur = self.con.cursor()
        self.createTable()

    def createTable(self):
        try:
             self.cur.execute("CREATE TABLE scores (user text, score integer)")
             self.con.commit()
        except:
            return
    
    def insertScore(self, user, score):
        self.cur.execute(f"INSERT INTO scores (user, score) values ('{user}', '{score}')")
        self.con.commit()

    def getScores(self):
        self.cur.execute(f"SELECT * FROM scores")
        return self.cur.fetchall()


# con = sqlite3.connect("score.db")
# cur = con.cursor()
# cur.execute(f"SELECT * FROM scores")
# print(cur.fetchall())


# conn.close()