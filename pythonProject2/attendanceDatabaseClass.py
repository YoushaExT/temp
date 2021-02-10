import sqlite3


class dbClass:
    def __init__(self, file):
        # conn = sqlite3.connect('attend5.db')
        self.conn = sqlite3.connect(file)
        self.c = self.conn.cursor()

    def print_user_info(self, uid=None, filter=True):
        # print all columns or few depending on filter
        if filter and uid:  # print 1 person with filter
            a = self.c.execute('select id, name, position, lastUpdate from person where id = ?',
                          (uid,))
        elif not filter and uid:  # print 1 person without filter
            a = self.c.execute('select * from person where id = ?', (uid,))
        elif filter and not uid:  # print everyone with filter
            a = self.c.execute('select id, name, position, lastUpdate from person')
        elif not filter and not uid:  # print everyone without filter
            a = self.c.execute('select * from person')

        # First row, column headings
        columns = ['Login ID', 'Name', 'Designation']
        if not filter:
            columns += ['Password', 'isAdmin', 'isSuperAdmin']
        columns.append('Updated by')

        # Print first row
        for col in columns:
            print(col, end=(13-len(col))*' ')
        print()

        # Print rest of the table, aligned
        for entry in a:
            for cell in entry:
                print(cell, end=(13-len(str(cell)))*' ')
            print()
