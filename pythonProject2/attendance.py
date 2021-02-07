import sqlite3

Admins = {}
Employees = {}


class Person:
    def __init__(self, person_id, name, position, pwd):
        self.name, self.position, self.person_id, self.pwd = name, position, person_id, pwd


class Admin(Person):
    def __init__(self, person_id, name, position, pwd):
        super().__init__(person_id, name, position, pwd)

    def menu(self, conn, c):
        choice = input('Press 1 to add a new Employee\n'
                       'Press 2 to add a new Admin\n'
                       'Press 3 to change an Employee\'s profile\n'
                       'Press 4 to mark your attendance\n'
                       'Press 5 to view all attendance records\n'
                       'Press 6 to delete a member\n'
                       'Press q to quit\n')
        if choice == '1':
            self.add_member(conn, c, 0)
        elif choice == '2':
            self.add_member(conn, c, 1)
        elif choice == '3':
            self.update_employee(conn, c)
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            self.delete_ppl(conn, c)
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
        c.execute('insert into person (id, name, position, pwd, isAdmin) values (?, ?, ?, ?, ?)',
                  (uid, name, position, pwd, admin))
        conn.commit()

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
        pass


class Employee(Person):
    def __init__(self, person_id, name, position, pwd):
        super().__init__(person_id, name, position, pwd)


def login(c):
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


def create_table_person(c):
    try:
        c.execute('CREATE TABLE person '
                  '(id VARCHAR(255) PRIMARY KEY,'
                  ' name VARCHAR(255),'
                  ' position VARCHAR(255),'
                  ' pwd VARCHAR(255),'
                  ' isAdmin BIT)')

    except sqlite3.Error:
        pass


def create_base_admin(conn, c):
    uid = input('Set login id of the admin:\n')
    while list(c.execute('select * from person where id = ?', (uid,))):
        print(f'User ID:{uid} already exists, provide a unique ID!')
        uid = input('Set login id of the admin:\n')
    pwd = input('Set password of the admin:\n')
    name = input('Set name:\n')
    position = input('Set position:\n')
    c.execute('insert into person (id, name, position, pwd, isAdmin) values (?, ?, ?, ?, 1)',
              (uid, name, position, pwd))
    conn.commit()


def show_table(c):
    a = c.execute('select * from person')
    # for e in a:  # print tuples
    #     print(e)
    for e in a:
        for cell in e:
            print(cell, end=' ')
        print()


def load(c):

    table = c.execute('select * from person')
    for entry in table:
        if entry[4] == 1:
            Admins[entry[0]] = (Admin(entry[0], entry[1], entry[2], entry[3]))
        elif entry[4] == 0:
            Employees[entry[0]] = (Employee(entry[0], entry[1], entry[2], entry[3]))
        print(entry)
    print(Admins, Employees)

def main():
    conn = sqlite3.connect('attend2.db')
    c = conn.cursor()
    create_table_person(c)
    show_table(c)
    if not list(c.execute('select * from person')):
        print('No base admin detected!\n Create a new base admin:')
        create_base_admin(conn, c)

    load(c)

    while True:
        lg = login(c)
        if lg[0]:
            break
        print('Invalid ID and/or Password!')
    print('Login successful')
    current_user = lg[1]
    print(current_user)
    if isinstance(current_user, Admin):
        print('Admin Menu:')
        while current_user.menu(conn, c):
            pass
    if isinstance(current_user, Employee):
        print('Employee Menu:')


if __name__ == '__main__':
    main()
