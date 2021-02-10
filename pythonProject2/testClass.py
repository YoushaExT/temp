from attendanceDatabaseClass import dbClass

def main():
    db = dbClass('attend5.db')
    db.print_user_info('admin1')
    db.print_user_info('admin1', False)
    pass


if __name__ == '__main__':
    main()