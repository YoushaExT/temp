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

    def show_table(self, option=2, uid=None):
        # 0 to display employees only, 1 to display admins only, else display all
        if option in (0, 1):
            if uid:
                a = self.c.execute('select * from person where isAdmin = ? and not id = ?'
                              , (option, uid))
            else:
                a = self.c.execute('select * from person where isAdmin = ?', (option,))
        else:
            if uid:
                a = self.c.execute('select * from person where not id = ?', (uid,))
            else:
                a = self.c.execute('select * from person')

        # First row, column headings
        columns = ['Login ID', 'Name', 'Designation', 'Password',
                   'isAdmin', 'isSuperAdmin', 'Updated By']

        # Print first row
        for col in columns:
            print(col, end=(13-len(col))*' ')
        print()

        # Print rest of the table, aligned
        for entry in a:
            for cell in entry:
                print(cell, end=(13-len(str(cell)))*' ')
            print()

    def create_date_table(self):
        try:
            self.c.execute('create table dates'
                      '(dateID INTEGER PRIMARY KEY AUTOINCREMENT,'
                      'date DATE);')
            self.conn.commit()
        except sqlite3.Error as e:
            # print(e)
            pass

    def create_presents_table(self):
        try:
            self.c.execute('create table presents'
                      '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                      'dateID INTEGER,'
                      'personID VARCHAR(255))')
            self.conn.commit()
        except sqlite3.Error as e:
            # print(e)
            pass

    def create_leaves_table(self):
        try:
            self.c.execute('create table leaves'
                      '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                      'dateID INTEGER,'
                      'personID VARCHAR(255))')
            self.conn.commit()
        except sqlite3.Error as e:
            # print(e)
            pass

    def create_table_person(self):
        try:
            self.c.execute('CREATE TABLE person '
                      '(id VARCHAR(255) PRIMARY KEY,'
                      ' name VARCHAR(255),'
                      ' position VARCHAR(255),'
                      ' pwd VARCHAR(255),'
                      ' isAdmin BIT,'
                      ' isSuperAdmin BIT DEFAULT 0,'
                      ' lastUpdate VARCHAR(255))')

        except sqlite3.Error as e:
            # print(e)
            pass
        self.conn.commit()

    def is_person_empty(self):
        if list(self.c.execute('select * from person')):
            return False
        return True

    def create_base_admin(self):
        uid = input('Set login id of the admin:\n')
        while list(self.c.execute('select * from person where id = ?', (uid,))):
            print(f'User ID:{uid} already exists, provide a unique ID!')
            uid = input('Set login id of the admin:\n')
        pwd = input('Set password of the admin:\n')
        name = input('Set name:\n')
        position = input('Set position:\n')
        self.c.execute('insert into person (id, name, position, pwd, isAdmin, lastUpdate, isSuperAdmin) '
                  'values (?, ?, ?, ?, 1, ?, 1)',
                  (uid, name, position, pwd, uid))
        self.conn.commit()

    def get_person_table(self):

        table = self.c.execute('select * from person')
        return list(table)
    # todo
    def update_name(self, updater_id, uid):

        x = input('Enter a new name:\n')
        self.c.execute('update person set name = ?, lastUpdate=? where id = ?', (x, updater_id, uid))
        self.conn.commit()

    def update_position(self, updater_id, uid):

        x = input('Enter a new position:\n')
        self.c.execute('update person set position = ?, lastUpdate=? where id = ?', (x, updater_id, uid))
        self.conn.commit()

    def update_password(self, updater_id, uid):

        x = input('Enter a new password:\n')
        self.c.execute('update person set pwd = ?, lastUpdate=? where id = ?', (x, updater_id, uid))
        self.conn.commit()

    def insert_date(self, date):

        a = self.c.execute('select date from dates where date = ?', (date,))
        # print(list(a))
        if not list(a):
            # print('Doesnt already exist')
            self.c.execute('insert into dates (date) values (?)', (date,))
            self.conn.commit()