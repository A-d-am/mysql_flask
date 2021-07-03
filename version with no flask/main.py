import pymysql
import settings


def menu(key):
    print("""
    Select the action you want to perform (choose the number): 
    1 -- Create a table with the columns 'id', 'full name' and 'position' 
    2 -- Create an employee record
    3 -- Get data from the table
    4 -- Update employee data
    5 -- Delete an employee record
    6 -- Delete a table 
    """)
    choice = input("Print your choice: ")
    try:
        if choice == '1':
            key.create_table()
        elif choice == '2':
            key.post()
        elif choice == '3':
            key.get()
        elif choice == '4':
            key.put()
        elif choice == '5':
            key.delete_worker()
        elif choice == '6':
            key.delete_table()
        elif choice == '7':
            return True
        else:
            print('Check the input and try again')
    except Exception as ex:
        print(ex)


class DataFirmu():
    def create_table(self):

        with connection.cursor() as cursor:
            create_table_query = "CREATE TABLE workers (id int AUTO_INCREMENT," \
                                 "name varchar(255), " \
                                 "position varchar(255), " \
                                 " PRIMARY KEY (id)); "
            cursor.execute(create_table_query)
            return 'Table created successful'

    def check_data(self, data):
        name, position = data
        # select  data from table
        with connection.cursor() as cursor:
            select_rows = f"SELECT * FROM workers WHERE name = '{name}'"
            cursor.execute(select_rows)
            rows = cursor.fetchall()
            for row in rows:
                check = row
                if check is None:
                    return False  # return False if there is no such record
                else:
                    return True  # return True if there is record with those name and position

    def check_data_id(self, id):
        with connection.cursor() as cursor:
            select_rows = 'SELECT * FROM workers WHERE id = ' + str(id)
            cursor.execute(select_rows)
            rows = cursor.fetchall()
            for row in rows:
                check = row
                if check is None:
                    return False  # return False if there is no such record
                else:
                    return True  # return True if there is record with this id

    def post(self):
        name = input("Write the worker's name: ").rstrip()
        employees_position = input("Write the employee's position: ").lower().strip()
        users_commit = input(
            f'Check that the data is correct: name = {name}, position = {employees_position}. If all correct,'
            f'print "+", else print "-": ')
        if users_commit == "+":
            # checking data
            cheking = self.check_data((name, employees_position))
            if cheking:
                user_choise = input(f'There is already a record with this data in your table: name = {name},'
                                    f' position = {employees_position}. Print "+" if you if you still want to make this entry,'
                                    f'else print "-": ')
                if user_choise == "+":
                    # insert data
                    with connection.cursor() as cursor:
                        insert_query = f"INSERT INTO workers (name, position) VALUES ('{name}', '{employees_position}')"
                        cursor.execute(insert_query)
                        connection.commit()
            else:
                # insert data
                with connection.cursor() as cursor:
                    insert_query = f"INSERT INTO workers (name, position) VALUES ('{name}', '{employees_position}')"
                    cursor.execute(insert_query)
                    connection.commit()
        elif users_commit == "-":
            print('The addition to the table was successfully canceled')
        else:
            print('Check the input and try again')

    def delete_worker(self):

        need_id = int(input('Enter the ID of the employee you want to remove from the table: '))
        with connection.cursor() as cursor:
            delete_query = 'DELETE FROM workers WHERE id = ' + str(need_id)
            cursor.execute(delete_query)
            connection.commit()
        print(f"The employee with id = {need_id} was removed from the table")

    def put(self):

        put_id = int(input('Enter the ID of the employee whose information you want to update in the table: '))
        checking = self.check_data_id(put_id)
        print('Write the new information about this worker')
        name = input("Write the worker's name: ").strip()
        employees_position = input("Write the employee's position: ").lower().strip()
        if checking:
            users_commit = input(
                f'Check that the data is correct: name = {name}, position = {employees_position}. If all correct,'
                f'print "+", else print "-": ')
            if users_commit == "+":
                with connection.cursor() as cursor:
                    update_query = f'UPDATE workers SET name = "{name}", position = "{employees_position}" WHERE id = {put_id} '
                    cursor.execute(update_query)
                    connection.commit()
        else:
            users_commit = input(
                f'Check that the data is correct: name = {name}, position = {employees_position}. If all correct,'
                f'print "+", else print "-": ')
            if users_commit == "+":
                with connection.cursor() as cursor:
                    insert_query = f"INSERT INTO workers (name, position) VALUES ('{name}', '{employees_position}')"
                    cursor.execute(insert_query)
                    connection.commit()
            else:
                pass

    def get(self):

        choose = input(
            'What do you want to get a selection for: by name, position, or the entire table. Choose between'
            ' "name", "position", "table" ').strip()
        if choose == 'name':
            get_name = input("Enter the employee's name: ")
            with connection.cursor() as cursor:
                get_query = f"SELECT * FROM workers WHERE name ='{get_name}'"
                cursor.execute(get_query)
                rows = cursor.fetchall()
                checking = self.check_data(get_name)
                if checking:
                    for row in rows:
                        print(row)
                else:
                    print(f"There is no record of an employee with the name '{get_name}' in the table")
        elif choose == "position":
            get_position = input("Enter the employee's position")
            with connection.cursor() as cursor:
                get_query = f"SELECT * FROM workers WHERE position ='{get_position}'"
                cursor.execute(get_query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        elif choose == "table":
            with connection.cursor() as cursor:
                get_query = f"SELECT * FROM workers "
                cursor.execute(get_query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        else:
            print("Input error, please try again")

    def delete_table(self):
        with connection.cursor() as cursor:
            delete_teble_query = "DROP TABLE workers"
            cursor.execute(delete_teble_query)
            connection.commit()
        print("The table was deleted successfully")


def try_to_connect():
    global connection
    connection = pymysql.connect(
        host=settings.host_name,
        user=settings.user_name,
        password=settings.user_password,
        database=settings.database,
        cursorclass=pymysql.cursors.DictCursor
    )

    return True


def main():
    try:
        try_to_connect()
        key = DataFirmu()
        flag = True
        while flag:
            temp = menu(key)
            if temp:
                flag = False
                print('Shutdown...')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
