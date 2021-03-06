import sqlite3

def main():
    conn = sqlite3.connect('testForeign.db')  # a db is created
    c = conn.cursor()
    # cursor can execute sql queries
    # createTable(c)
    # c.execute('insert into students (first, middle, last, house, birth) values (?,?,?,?,?)',
    #           ('yousha', 'arshad', 'shamsi', 'iqbal', '1996'))

    # c.execute('update students set first=? where id=?', ('yous', '1'))
    # conn.commit()

    choice = int(input('Press 1 to create a new entry:\n'
                       'Press 2 to display all existing students:\n'
                       'Press 3 to delete an existing entry:\n'
                       'Press 4 to update an existing entry:\n'
                       'Press 5 to display by id\n'))

    if choice == 1:
        newEntry(c)
    elif choice == 2:
        displayEntries(c)
    elif choice == 3:
        deleteEntry(c)
    elif choice == 4:
        updateEntry(c)
    elif choice == 5:
        display_by_id(c)
    conn.commit()
    pass

def createTable(c):
    # c.execute('CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, first VARCHAR(255))')
    try:
        c.execute('CREATE TABLE students '
                  '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  ' first VARCHAR(255),'
                  ' house VARCHAR(10),'
                  ' birth INTEGER)')

        c.execute('CREATE TABLE orders'
                  '(orderID INTEGER PRIMARY KEY AUTOINCREMENT'
                  'studentID INTEGER FOREIGN KEY REFERENCES students (id) ON DELETE CASCADE')

    except sqlite3.Error as e:
        print(e)

def newEntry(c):
    f_name = input('Enter the student\'s first name: ')
    m_name = input('Enter the student\'s middle name: ')
    l_name = input('Enter the student\'s last name: ')
    house = input('Enter the student\'s house name: ')
    birth = input('Enter the student\'s birth year: ')

    c.execute('insert into students (first, middle, last, house, birth) values (?,?,?,?,?)',
              (f_name, m_name, l_name, house, birth))
    print(f_name, m_name, l_name, house, birth)

def displayEntries(c):
    entries = c.execute('select * from students')
    # print(list(entries))
    for entry in entries:
        print(entry)

def deleteEntry(c):
    displayEntries(c)
    id = int(input('Enter the id to delete:\n'))
    c.execute('delete from students where id = ?', (id,))

def updateEntry(c):
    def get_choice():
        choice = input('Press 1 to update first name\n'
                       'Press 2 to update middle name\n'
                       'Press 3 to update last name\n'
                       'Press 4 to update house\n'
                       'Press 5 to update birth year\n'
                       'Press q when done\n')
        return choice
    def first(id):
        x = input('Enter a new first name:\n')
        print(x, id)
        c.execute('update students set first=? where id=?', (x, id))

    def middle(id):
        x = input('Enter a new middle name:\n')
        c.execute('update students set middle=? where id=?', (x, id))

    def last(id):
        x = input('Enter a new middle name:\n')
        c.execute('update students set last=? where id=?', (x, id))

    def house(id):
        x = input('Enter a new house name:\n')
        c.execute('update students set house=? where id=?', (x, id))

    def birth(id):
        x = input('Enter a new birth name:\n')
        c.execute('update students set birth=? where id=?', (x, id))

    displayEntries(c)
    id = int(input('Enter the id to update: \n'))
    ch = get_choice()
    while ch != 'q':
        if ch == '1':
            first(id)
            print('done')
        elif ch == '2':
            middle(id)
        elif ch == '3':
            last(id)
        elif ch == '4':
            house(id)
        elif ch == '5':
            birth(id)
        ch = get_choice()
    print('Updated Table:')
    displayEntries(c)


def display_by_id(c):
    uid = int(input('Enter id:\n'))
    # print(uid, type(uid))
    entry = c.execute('select first from students where id = ?', (uid,))
    # if list(entry):
    #     print('Exists')
    # else:
    #     print('None')
    # print(list(entry), entry, type(entry))
    for e in entry:
        print(e, type(e), e[0])

if __name__ == '__main__':
    main()