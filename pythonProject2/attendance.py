import sqlite3
import datetime

Admins = {}
Employees = {}
TODAY = datetime.datetime.now().date()


class Person:
    def __init__(self, person_id, name, position, pwd):
        self.name, self.position, self.person_id, self.pwd = name, position, person_id, pwd

    def update_name(self, conn, c, uid):
        print_user_info(c, uid)
        x = input('Enter a new name:\n')
        c.execute('update person set name = ?, lastUpdate=? where id = ?', (x, self.person_id, uid))
        print_user_info(c, uid)
        conn.commit()

    def update_position(self, conn, c, uid):
        print_user_info(c, uid)
        x = input('Enter a new position:\n')
        c.execute('update person set position = ?, lastUpdate=? where id = ?', (x, self.person_id, uid))
        print_user_info(c, uid)
        conn.commit()

    def update_password(self, conn, c, uid):
        print_user_info(c, uid)
        x = input('Enter a new password:\n')
        c.execute('update person set pwd = ?, lastUpdate=? where id = ?', (x, self.person_id, uid))
        print_user_info(c, uid)
        conn.commit()

    def mark_present(self, conn, c, date):
        uid = self.person_id
        insert_date(date, conn, c)
        a = c.execute('select dateID from dates where date = ?', (date,))
        did = list(a)[0][0]  # dateID
        print(did, date)
        c.execute('insert into presents (dateID, personID) values (?, ?)', (did, uid))
        conn.commit()

    def mark_leave(self, conn, c, date):
        uid = self.person_id
        insert_date(date, conn, c)
        a = c.execute('select dateID from dates where date = ?', (date,))
        did = list(a)[0][0]  # dateID
        print(did, date)
        c.execute('insert into leaves (dateID, personID) values (?, ?)', (did, uid))
        conn.commit()

    def update_self(self, conn, c):
        print('Update menu:')
        def choicePrompt():
            choice = input('Press 1 to change name\n'
                           'Press 2 to change position\n'
                           'Press 3 to change password\n'
                           'Press 4 to view your profile info\n'
                           'Press q when done\n')
            return choice
        self.show_self(c, True)
        uid = self.person_id

        while True:
            choice = choicePrompt()
            if choice == '1':
                self.update_name(conn, c, uid)
            elif choice == '2':
                self.update_position(conn, c, uid)
            elif choice == '3':
                self.update_password(conn, c, uid)
            elif choice == 'q':
                break

        self.show_self(c, True)

    def show_self(self, c, filter=False):
        if not filter:
            a = c.execute('select * from person where id = ?', (self.person_id,))
        else:
            a = c.execute('select id, name, position, lastUpdate from person where id = ?',
                          (self.person_id,))

        # todo saaf suthra print
        columns = ['Login ID', 'Name', 'Designation', 'Updated By']

        for col in columns:
            print(col, end=(12-len(col))*' ')
        print()

        for entry in a:
            for i, cell in enumerate(entry):
                print(cell, end=(12-len(str(cell)))*' ')
            print()

class Admin(Person):
    def __init__(self, person_id, name, position, pwd):
        super().__init__(person_id, name, position, pwd)

    def menu(self, conn, c):
        insert_date(TODAY, conn, c)
        a = c.execute('select dateID from dates where date = ?', (TODAY,))
        did = list(a)[0][0]  # dateID
        s_p, s_l, marked = '', '', True

        b = c.execute('select * from presents where dateID=? and personID=?', (did, self.person_id))
        bcopy = list(b)
        d = c.execute('select * from leaves where dateID=? and personID=?', (did, self.person_id))
        dcopy = list(d)
        # print(bcopy, dcopy, self.person_id, did, type(did))
        if not bcopy and not dcopy:
            # not already marked
            marked = False
            s_p = 'Press p to mark present for today\n'
            s_l = 'Press l to mark leave for today\n'
        print('ADMIN MENU:')
        print(TODAY, TODAY.strftime('%A'))
        choice = input('Press 1 to add a new Employee\n'
                       'Press 2 to add a new Admin\n'
                       'Press 3 to change an Employee\'s profile\n'
                       'Press 4 to view all attendance records\n'
                       'Press 5 to delete a member\n'
                       'Press 6 to change your profile info\n'
                       'Press 7 to view your own profile info\n'
                       'Press o to logout\n'
                       f'{s_p}{s_l}Press q to quit\n')
        if choice == '1':
            self.add_member(conn, c, 0)
        elif choice == '2':
            self.add_member(conn, c, 1)
        elif choice == '3':
            self.update_employee(conn, c)
        elif choice == '4':
            self.view_attendance_all(conn, c)
        elif choice == '5':
            self.delete_ppl(conn, c)
        elif choice == '6':
            self.update_self(conn, c)
        elif choice == '7':
            self.show_self(c, True)
        elif choice == 'p' and not marked:
            self.mark_present(conn, c, TODAY)
        elif choice == 'l' and not marked:
            self.mark_leave(conn, c, TODAY)
        elif choice == 'o':
            login_menu(conn, c)
            return False
        elif choice == 'q':
            return False
        return True  # True to keep asking, False to exit
        # can add members
        # can change employee profile (update last column to show which admin updated)
        # can mark his own attendance {inherit?}
        # can view attendance records of all employees+admins

    def add_member(self, conn, c, admin):
        uid = input('Set login:\n')
        while list(c.execute('select * from person where id = ?', (uid,))):
            print(f'User ID:{uid} already exists, provide a unique ID!')
            uid = input('Set login id:\n')
        pwd = input('Set password:\n')
        name = input('Set name:\n')
        position = input('Set position:\n')
        c.execute('insert into person (id, name, position, pwd, isAdmin, lastUpdate) '
                  'values (?, ?, ?, ?, ?, ?)',
                  (uid, name, position, pwd, admin, self.person_id))
        conn.commit()
        # also update dict
        if admin == 1:
            Admins[uid] = Admin(uid, name, position, pwd)
        elif admin == 0:
            Employees[uid] = Employee(uid, name, position, pwd)

    def delete_ppl(self, conn, c):
        show_table(c)
        uid = input('Which id to delete? (Press q to skip):\n')
        while not list(c.execute('select * from person where id = ?', (uid,))):
            if uid == 'q':
                break
            print(f'No account with id: {uid} exists in the table!')
            uid = input('Which id to delete? (Press q to skip):\n')
        c.execute('delete from person where id = ?', (uid,))
        conn.commit()
        show_table(c)
        # also update python dicts to remove the deleted item
        if uid in Admins:
            Admins.pop(uid)
        elif uid in Employees:
            Employees.pop(uid)

    def update_employee(self, conn, c):
        print('Update menu:')
        def choicePrompt():
            choice = input('Press 1 to change name\n'
                           'Press 2 to change position\n'
                           'Press 3 to change password\n'
                           'Press q when done\n')
            return choice
        show_table(c, 0)  # show only employees
        uid = input('Which id to update? (Press q to skip):\n')
        while uid not in Employees:
            if uid == 'q':
                return
            print(f'No employee account with id: {uid} exists in the table!')
            uid = input('Which id to update? (Press q to skip):\n')

        while True:
            choice = choicePrompt()
            if choice == '1':
                self.update_name(conn, c, uid)
            elif choice == '2':
                self.update_position(conn, c, uid)
            elif choice == '3':
                self.update_password(conn, c, uid)
            elif choice == 'q':
                break

        # conn.commit()
        show_table(c)


    def view_attendance_all(self, conn, c):
        ds = c.execute('select * from dates')
        ds = list(ds)
        # print(list(ds))
        # for each date -> for each person
        print('ATTENDANCE RECORDS:')
        print('Date: \t\t', end='')
        for d in ds:
            print(d[1], end=' ')
        print()
        ps = list(c.execute('select id from person'))
        for p in ps:
            person = p[0]
            print(person, end='\t\t')
            for d in ds:
                did = d[0]
                if list(c.execute('select * from presents where dateID=? and personID=?', (did, person))):
                    print('Present', end=4*' ')
                elif list(c.execute('select * from leaves where dateID=? and personID=?', (did, person))):
                    print('Leave', end=6*' ')
                else:
                    print('Absent', end=5*' ')
            print()


class Employee(Person):
    def __init__(self, person_id, name, position, pwd):
        super().__init__(person_id, name, position, pwd)

    def menu(self, conn, c):
        insert_date(TODAY, conn, c)
        a = c.execute('select dateID from dates where date = ?', (TODAY,))
        did = list(a)[0][0]  # dateID
        s_p, s_l, marked = '', '', True

        b = c.execute('select * from presents where dateID=? and personID=?', (did, self.person_id))
        bcopy = list(b)
        d = c.execute('select * from leaves where dateID=? and personID=?', (did, self.person_id))
        dcopy = list(d)

        if not bcopy and not dcopy:
            # not already marked
            marked = False
            s_p = 'Press p to mark present for today\n'
            s_l = 'Press l to mark leave for today\n'
        print('EMPLOYEE MENU:')
        print(TODAY, TODAY.strftime('%A'))
        choice = input('Press 1 to view your attendance record\n'
                       'Press 2 to change your profile info\n'
                       'Press 3 to view your own profile info\n'
                       'Press o to logout\n'
                       f'{s_p}{s_l}Press q to quit\n')
        if choice == '1':
            self.view_own_attendance(conn, c)
        elif choice == '2':
            self.update_self(conn, c)
        elif choice == '3':
            self.show_self(c, True)
        elif choice == 'p' and not marked:
            self.mark_present(conn, c, TODAY)
        elif choice == 'l' and not marked:
            self.mark_leave(conn, c, TODAY)
        elif choice == 'o':
            login_menu(conn, c)
            return False
        elif choice == 'q':
            return False
        return True

    def view_own_attendance(self, conn, c):
        ds = c.execute('select * from dates')
        ds = list(ds)

        # print first row, begin
        print('ATTENDANCE RECORDS:')
        print('Date: \t\t', end='')
        for d in ds:
            print(d[1], end=' ')
        print()
        # print first row, end

        person = self.person_id
        print(person, end='\t\t')
        for d in ds:
            did = d[0]
            # if present is marked for this date
            if list(c.execute('select * from presents where dateID=? and personID=?', (did, person))):
                print('Present', end=4*' ')
            # if leave is marked for this date
            elif list(c.execute('select * from leaves where dateID=? and personID=?', (did, person))):
                print('Leave', end=6*' ')
            # if not marked for this date
            else:
                print('Absent', end=5*' ')
        print()

def login(c):
    print('LOGIN')
    in_id = input('Enter your id:\n')
    in_pwd = input('Enter your password:\n')
    if in_id in Admins:
        # if password match
        if in_pwd == Admins[in_id].pwd:
            return True, Admins[in_id]
    elif in_id in Employees:
        if in_pwd == Employees[in_id].pwd:
            return True, Employees[in_id]
    return False, None


def create_table_person(conn, c):
    try:
        c.execute('CREATE TABLE person '
                  '(id VARCHAR(255) PRIMARY KEY,'
                  ' name VARCHAR(255),'
                  ' position VARCHAR(255),'
                  ' pwd VARCHAR(255),'
                  ' isAdmin BIT,'
                  ' lastUpdate VARCHAR(255))')

    except sqlite3.Error:
        pass
    conn.commit()


def create_base_admin(conn, c):
    uid = input('Set login id of the admin:\n')
    while list(c.execute('select * from person where id = ?', (uid,))):
        print(f'User ID:{uid} already exists, provide a unique ID!')
        uid = input('Set login id of the admin:\n')
    pwd = input('Set password of the admin:\n')
    name = input('Set name:\n')
    position = input('Set position:\n')
    c.execute('insert into person (id, name, position, pwd, isAdmin, lastUpdate) '
              'values (?, ?, ?, ?, 1, ?)',
              (uid, name, position, pwd, uid))
    conn.commit()


def show_table(c, option=2):
    # 0 to display employees only, 1 to display admins only, else display all
    if option in (0, 1):
        a = c.execute('select * from person where isAdmin = ?', (option,))
    else:
        a = c.execute('select * from person')
    for e in a:
        for cell in e:
            print(cell, end=' ')
        print()


def print_user_info(c, uid):
    a = c.execute('select * from person where id = ?', (uid,))
    for cell in a:
        print(cell, end=' ')
    print()


def load(c):
    table = c.execute('select * from person')
    for entry in table:
        if entry[4] == 1:
            Admins[entry[0]] = (Admin(entry[0], entry[1], entry[2], entry[3]))
        elif entry[4] == 0:
            Employees[entry[0]] = (Employee(entry[0], entry[1], entry[2], entry[3]))
        # print(entry)
    print('For testing, List of all admins and Employees:')
    print(Admins)
    print(Employees)


def create_date_table(conn, c):
    try:
        c.execute('create table dates'
                  '(dateID INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'date DATE);')
        conn.commit()
    except sqlite3.Error:
        pass


def insert_date(date, conn, c):

    a = c.execute('select date from dates where date = ?', (date,))
    # print(list(a))
    if not list(a):
        # print('Doesnt already exist')
        c.execute('insert into dates (date) values (?)', (date,))
        conn.commit()


def create_presents_table(conn, c):
    try:
        c.execute('create table presents'
                  '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'dateID INTEGER,'
                  'personID VARCHAR(255))')
        conn.commit()
    except sqlite3.Error as e:
        pass


def create_leaves_table(conn, c):
    try:
        c.execute('create table leaves'
                  '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'dateID INTEGER,'
                  'personID VARCHAR(255))')
        conn.commit()
    except sqlite3.Error as e:
        pass


def login_menu(conn, c):
    load(c)
    while True:
        lg = login(c)
        if lg[0]:
            break
        print('Invalid ID and/or Password!')
    print('Login successful')
    current_user = lg[1]
    print(f'Welcome {current_user.name}!')
    if isinstance(current_user, Admin):
        while current_user.menu(conn, c):
            pass
    if isinstance(current_user, Employee):
        while current_user.menu(conn, c):
            pass


def main():
    conn = sqlite3.connect('attend4.db')
    c = conn.cursor()
    create_table_person(conn, c)

    create_date_table(conn, c)
    create_presents_table(conn, c)
    create_leaves_table(conn, c)

    print('For testing: Person Table')
    show_table(c)
    if not list(c.execute('select * from person')):
        print('No base admin detected!\n Create a new base admin:')
        create_base_admin(conn, c)
    login_menu(conn, c)


def test_advance_one_day():
    global TODAY
    TODAY += datetime.timedelta(days=1)

# for testing - to change today's date
def test_retreat_one_day():
    global TODAY
    TODAY -= datetime.timedelta(days=1)


if __name__ == '__main__':
    # view_all()
    # test_advance_one_day()
    # test_retreat_one_day()
    main()