from attendanceDatabaseClass import dbClass

def main():
    db = dbClass('attend5.db')
    db.print_user_info('admin1')
    db.print_user_info('admin1', False)
    db2 = dbClass('testAttend.db')
    db2.create_date_table()
    db2.create_leaves_table()
    db2.create_presents_table()
    db2.create_table_person()
    pass


if __name__ == '__main__':
    main()