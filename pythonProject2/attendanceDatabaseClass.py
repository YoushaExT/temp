import sqlite3


class dbClass:
    def __init__(self, file):
        # conn = sqlite3.connect('attend5.db')
        self.conn = sqlite3.connect(file)
        self.c = self.conn.cursor()

    def print_user_info(self, uid):
        a = self.c.execute('select * from person where id = ?', (uid,))
        for cell in a:
            print(cell, end=' ')
        print()