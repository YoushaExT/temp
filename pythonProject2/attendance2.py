import datetime
from attendanceDatabaseClass import DbClass

SuperAdmins = {}
Admins = {}
Employees = {}
TODAY = datetime.datetime.now().date()


class Person:
    def __init__(self, person_id, name, position, pwd, db):
        self.name, self.position, self.person_id, self.pwd = name, position, person_id, pwd
        self.db = db

    def update_name(self, uid):

        self.db.print_user_info(uid)
        # updater, updated
        self.db.update_name(self.person_id, uid)
        self.db.print_user_info(uid)

    def update_position(self, uid):

        self.db.print_user_info(uid)
        # updater, updated
        self.db.update_position(self.person_id, uid)
        self.db.print_user_info(uid)

    def update_password(self, uid):

        self.db.print_user_info(uid)
        # updater, updated
        self.db.update_password(self.person_id, uid)
        self.db.print_user_info(uid)

    def mark_present(self, date):
        uid = self.person_id
        did = self.db.get_date_id(date)
        self.db.insert_present(did, uid)

    def mark_leave(self, date):
        uid = self.person_id
        did = self.db.get_date_id(date)
        self.db.insert_leave(did, uid)

    def update_self(self):
        print('Update menu:')

        def choice_prompt():
            ch = input('Press 1 to change name\n'
                       'Press 2 to change position\n'
                       'Press 3 to change password\n'
                       'Press 4 to view your profile info\n'
                       'Press q when done\n')
            return ch

        self.show_self()  # second argument is filter, if false will also display password
        uid = self.person_id

        while True:
            choice = choice_prompt()
            if choice == '1':
                self.update_name(uid)
            elif choice == '2':
                self.update_position(uid)
            elif choice == '3':
                self.update_password(uid)
            elif choice == 'q':
                break

        self.show_self()

    def show_self(self, my_filter=True):
        self.db.print_user_info(self.person_id, my_filter)


class Admin(Person):
    def __init__(self, person_id, name, position, pwd, db):
        super().__init__(person_id, name, position, pwd, db)

    def menu(self):
        did = self.db.get_date_id(TODAY)
        s_p, s_l, marked = '', '', True

        if self.db.check_absent(did, self.person_id):
            # not already marked
            marked = False
            s_p = 'Press p to mark present for today\n'
            s_l = 'Press l to mark leave for today\n'
        print('ADMIN MENU:')
        print(TODAY, TODAY.strftime('%A'))
        choice = input('Press 1 to add a new Employee\n'
                       'Press 2 to change an Employee\'s profile\n'
                       'Press 3 to view all attendance records\n'
                       'Press 4 to delete an Employee\n'
                       'Press 5 to change your profile info\n'
                       'Press 6 to view your own profile info\n'
                       'Press 7 to view all profiles\n'
                       'Press o to logout\n'
                       f'{s_p}{s_l}Press q to quit\n')
        if choice == '1':
            self.add_member(0)
        elif choice == '2':
            self.update_employee()
        elif choice == '3':
            self.view_attendance_all()
        elif choice == '4':
            self.delete_member()
        elif choice == '5':
            self.update_self()
        elif choice == '6':
            self.show_self()
        elif choice == '7':
            self.show_all()
        elif choice == 'p' and not marked:
            self.mark_present(TODAY)
        elif choice == 'l' and not marked:
            self.mark_leave(TODAY)
        elif choice == 'o':
            main()
            return False
        elif choice == 'q':
            return False
        return True  # True to keep asking, False to exit

    def add_member(self, admin):
        uid = input('Set login:\n')
        while self.db.does_person_exist(uid):
            print(f'User ID:{uid} already exists, provide a unique ID!')
            uid = input('Set login id:\n')
        pwd = input('Set password:\n')
        name = input('Set name:\n')
        position = input('Set position:\n')

        self.db.insert_person(uid, name, position, pwd, admin, self.person_id)
        # also update dict
        if admin == 1:
            Admins[uid] = Admin(uid, name, position, pwd, self.db)
        elif admin == 0:
            Employees[uid] = Employee(uid, name, position, pwd, self.db)

    def delete_member(self, su=False):
        # will show all admins except the current admin

        if not su:
            self.db.show_table(0)
            uid = input('Which id to delete? (Press q to skip):\n')
            while not self.db.does_person_exist(uid):
                if uid == 'q':
                    # break
                    return
                print(f'No employee account with id: {uid} exists in the table!')
                uid = input('Which id to delete? (Press q to skip):\n')
        else:
            self.db.show_table(1, self.person_id)
            uid = input('Which id to delete? (Press q to skip):\n')

            while uid == self.person_id:
                print('Cannot delete self, Provide another id!')
                uid = input('Which id to delete? (Press q to skip):\n')
            while not self.db.does_person_exist(uid):
                if uid == 'q':
                    # break
                    return
                print(f'No employee account with id: {uid} exists in the table!')
                uid = input('Which id to delete? (Press q to skip):\n')

                while uid == self.person_id:
                    print('Cannot delete self, Provide another id!')
                    uid = input('Which id to delete? (Press q to skip):\n')

        self.db.delete_person(uid)

        # show either employee table or admin table excluding super admin
        self.db.show_table(1, self.person_id) if su else self.db.show_table(0)

        # also update python dicts to remove the deleted item
        if uid in Admins:
            Admins.pop(uid)
        elif uid in Employees:
            Employees.pop(uid)

    def update_employee(self):
        print('Update menu:')

        def choice_prompt():
            ch = input('Press 1 to change name\n'
                       'Press 2 to change position\n'
                       'Press 3 to change password\n'
                       'Press q when done\n')
            return ch

        self.db.show_table(0)  # show only employees
        uid = input('Which id to update? (Press q to skip):\n')
        while uid not in Employees:
            if uid == 'q':
                return
            print(f'No employee account with id: {uid} exists in the table!')
            uid = input('Which id to update? (Press q to skip):\n')

        while True:
            choice = choice_prompt()
            if choice == '1':
                self.update_name(uid)
            elif choice == '2':
                self.update_position(uid)
            elif choice == '3':
                self.update_password(uid)
            elif choice == 'q':
                break

        self.db.show_table()

    def view_attendance_all(self):

        ds = self.db.get_dates_table()

        # First 2 rows
        print('ATTENDANCE RECORDS:')
        print('Date: \t\t', end='')
        for d in ds:
            print(d[1], end=' ')
        print()

        ps = self.db.get_all_person_ids()
        # for each person -> for each date
        for p in ps:
            person = p[0]
            print(person, end='\t\t')
            for d in ds:
                did = d[0]
                # print present/absent/leave, aligned
                if self.db.check_present(did, person):
                    print('Present', end=4 * ' ')
                elif self.db.check_leave(did, person):
                    print('Leave', end=6 * ' ')
                else:
                    print('Absent', end=5 * ' ')
            print()

    def show_all(self, my_filter=True):
        self.db.print_user_info(my_filter=my_filter)


class Employee(Person):
    def __init__(self, person_id, name, position, pwd, db):
        super().__init__(person_id, name, position, pwd, db)

    def menu(self):
        did = self.db.get_date_id(TODAY)
        s_p, s_l, marked = '', '', True

        # if absent (not marked yet)
        if self.db.check_absent(did, self.person_id):
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
            self.view_own_attendance()
        elif choice == '2':
            self.update_self()
        elif choice == '3':
            self.show_self()
        elif choice == 'p' and not marked:
            self.mark_present(TODAY)
        elif choice == 'l' and not marked:
            self.mark_leave(TODAY)
        elif choice == 'o':
            main()
            return False
        elif choice == 'q':
            return False
        return True

    def view_own_attendance(self):
        ds = self.db.get_dates_table()

        # print first row, begin
        print('ATTENDANCE RECORDS:')
        print('Date: \t\t', end='')
        for d in ds:
            print(d[1], end=' ')
        print()
        # print first row, end

        person = self.person_id
        print(person, end='\t\t')
        # for just 1 person -> for each date
        for d in ds:
            did = d[0]
            # if a present is marked for this date
            if self.db.check_present(did, person):
                print('Present', end=4 * ' ')
            # if a leave is marked for this date
            elif self.db.check_leave(did, person):
                print('Leave', end=6 * ' ')
            # if not marked for this date
            else:
                print('Absent', end=5 * ' ')
        print()


class SuperAdmin(Admin):
    def __init__(self, person_id, name, position, pwd, db):
        super().__init__(person_id, name, position, pwd, db)

    def menu(self):
        did = self.db.get_date_id(TODAY)
        s_p, s_l, marked = '', '', True

        if self.db.check_absent(did, self.person_id):
            # not already marked
            marked = False
            s_p = 'Press p to mark present for today\n'
            s_l = 'Press l to mark leave for today\n'

        print('SUPER ADMIN MENU:')
        print(TODAY, TODAY.strftime('%A'))
        choice = input('Press 1 to add a new Admin\n'
                       'Press 2 to view all attendance records\n'
                       'Press 3 to delete an Admin\n'
                       'Press 4 to change your profile info\n'
                       'Press 5 to view your own profile info\n'
                       'Press 6 to view all profiles\n'
                       'Press o to logout\n'
                       f'{s_p}{s_l}Press q to quit\n')

        if choice == '1':
            self.add_member(1)
        elif choice == '2':
            self.view_attendance_all()
        elif choice == '3':
            self.delete_member(True)
        elif choice == '4':
            self.update_self()
        elif choice == '5':
            self.show_self()
        elif choice == '6':
            self.show_all()
        elif choice == 'p' and not marked:
            self.mark_present(TODAY)
        elif choice == 'l' and not marked:
            self.mark_leave(TODAY)
        elif choice == 'o':
            main()
            return False
        elif choice == 'q':
            return False
        return True  # True to keep asking, False to exit


def login():
    print('LOGIN')
    in_id = input('Enter your id:\n')
    in_pwd = input('Enter your password:\n')

    if in_id in SuperAdmins:
        if in_pwd == SuperAdmins[in_id].pwd:
            return True, SuperAdmins[in_id]

    elif in_id in Admins:
        # if password match
        if in_pwd == Admins[in_id].pwd:
            return True, Admins[in_id]
    elif in_id in Employees:
        if in_pwd == Employees[in_id].pwd:
            return True, Employees[in_id]
    return False, None


def login_menu(database_builder):
    database_builder.load()
    while True:
        lg = login()
        if lg[0]:
            break
        print('Invalid ID and/or Password!')
    print('Login successful')
    current_user = lg[1]
    print(f'Welcome {current_user.name}!')

    while current_user.menu():
        pass


class AttendanceDatabaseBuilder:
    def __init__(self, database_name):
        self.db = DbClass(database_name)
        self.load()

    def show_table(self, option=2, uid=None):
        self.db.show_table(option, uid)

    def create_all_tables(self):
        # person
        self.db.create_table_person()
        # date
        self.db.create_date_table()
        # presents
        self.db.create_presents_table()
        # leaves
        self.db.create_leaves_table()
        pass

    def does_super_admin_exist(self):
        return self.db.does_super_admin_exist()

    def create_base_admin(self):
        self.db.create_base_admin()

    def load(self):
        self.db.insert_date(TODAY)
        table = self.db.get_person_table()
        for entry in table:
            if entry[5] == 1:
                SuperAdmins[entry[0]] = (SuperAdmin(entry[0], entry[1], entry[2], entry[3], self.db))
            if entry[4] == 1:
                Admins[entry[0]] = (Admin(entry[0], entry[1], entry[2], entry[3], self.db))
            elif entry[4] == 0:
                Employees[entry[0]] = (Employee(entry[0], entry[1], entry[2], entry[3], self.db))
        print('For testing, List of all admins and Employees:')
        print(Admins)
        print(Employees)

    def insert_date(self, date):

        self.db.insert_date(date)


def main():
    database_builder = AttendanceDatabaseBuilder('testAttend.db')
    database_builder.create_all_tables()

    print('For testing: Person Table')
    database_builder.show_table()

    if database_builder.does_super_admin_exist():
        print('No base admin detected!\n Create a new base admin:')
        database_builder.create_base_admin()
    login_menu(database_builder)


def test_advance_days(days=1):
    global TODAY
    TODAY += datetime.timedelta(days=days)


# for testing - to change today's date
def test_retreat_days(days=1):
    global TODAY
    TODAY -= datetime.timedelta(days=days)


if __name__ == '__main__':
    # test_advance_days()
    # test_retreat_days()
    main()
