import sqlite3


class Person:
    def __init__(self, name, position, person_id, pwd):
        self.name, self.position, self.person_id, self.pwd = name, position, person_id, pwd


class Admin(Person):
    def __init__(self, name, position, person_id, pwd):
        super().__init__(name, position, person_id, pwd)


def login(c):
    in_id = input('Enter your id:\n')
    in_pwd = input('Enter your password:\n')
    result = c.execute('select pwd from person where id = ?', (in_id,))
    # print(list(result))
    a = list(result).copy()
    # print(a, a[0], a[0][0])
    if a[0][0] == in_pwd:
        return True
    print('Invalid ID and/or password!')
    return False


def create_table_person(c):
    try:
        c.execute('CREATE TABLE person '
                  '(id VARCHAR(255) PRIMARY KEY,'
                  ' name VARCHAR(255),'
                  ' position VARCHAR(255),'
                  ' pwd VARCHAR(255))')

    except sqlite3.Error:
        pass


def create_base_admin(conn, c):
    uid = input('Set login id of the base admin:\n')
    while list(c.execute('select * from person where id = ?', (uid,))):
        print(f'User ID:{uid} already exists, provide a unique ID!')
        uid = input('Set login id of the base admin:\n')
    pwd = input('Set password of the base admin:\n')
    name = input('Set name:\n')
    position = input('Set position:\n')
    c.execute('insert into person (id, name, position, pwd) values (?, ?, ?, ?)',
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


def delete_ppl(conn, c):
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


def main():
    conn = sqlite3.connect('attend.db')
    c = conn.cursor()
    show_table(c)
    if not list(c.execute('select * from person')):
        print('No base admin detected!\n Create a new base admin:')
        create_base_admin(conn, c)
    # create_table_person(c)
    # conn.commit  # note: commit not working for actions performed in other functions
    a = c.execute('select * from person')
    for e in a:
        print(e)
    while True:
        if login(c):
            break
    print('Login successful')
    choice = input('Press 1 to delete a user:\n'
                   'Press q to exit:\n')
    if choice == '1':
        delete_ppl(conn, c)
    elif choice == 'q':
        return
    # y = Admin('Yousha', 'intern', 'yousha123', '12345')
    # print(y.name, y.position, y.person_id, y.pwd)


if __name__ == '__main__':
    main()
