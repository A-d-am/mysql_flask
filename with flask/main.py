from flask import Flask
from flask_restful import Api, Resource, reqparse
import settings
import pymysql

app = Flask(__name__)
api = Api(app)


class Workers(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("position")
        params = parser.parse_args()
        return my_data.post_data(params["id"], params["name"], params["position"])

    def get(self, id):
        return my_data.get_data(id)

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("position")
        params = parser.parse_args()
        return my_data.put_data(params["id"], params["name"], params["position"])

    def delete(self, id):
        return my_data.delete_data(id)


class Database:
    def post_data(self, worker_id, name, employees_position):
        checking = self.check_data(worker_id)
        if checking:
            return f'User with id {worker_id} already exists', 400
        else:
            with connection.cursor() as cursor:
                post_query = f"INSERT INTO workers (name,position) VALUES ('{name}', '{employees_position}') "
                cursor.execute(post_query)
                connection.commit()
            return self.rework_data(worker_id, name, employees_position), 201

    def get_data(self, worker_id):
        checking = self.check_data(worker_id)
        if checking:
            with connection.cursor() as cursor:
                get_query = f"SELECT * FROM workers WHERE id = {worker_id}"
                cursor.execute(get_query)
                rows = cursor.fetchall()
                for row in rows:
                    name = row['name']
                    position = row['position']
            return self.rework_data(worker_id, name, position)
        else:
            return 'Worker not found', 404

    def put_data(self, worker_id, name, employees_position):
        checking = self.check_data(worker_id)
        if checking:
            with connection.cursor() as cursor:
                update_query = f"UPDATE workers SET name = '{name}', " \
                               f"position = '{employees_position}' WHERE id = {worker_id} "
            cursor.execute(update_query)
            connection.commit()
            return self.rework_data(worker_id, name, employees_position), 200
        else:
            return self.post_data(worker_id, name, employees_position)

    def delete_data(self, worker_id):
        checking = self.check_data(worker_id)
        if checking:
            with connection.cursor() as cursor:
                delete_query =f"DELETE FROM workers WHERE id = {worker_id}"
                cursor.execute(delete_query)
                connection.commit()
            return f'Worker with id {worker_id} is deleted.', 201
        else:
            return 'Worker not found', 404

    def check_data(self, worker_id):
        with connection.cursor() as cursor:
            check_query = f"SELECT * FROM workers WHERE id = {worker_id}"
            cursor.execute(check_query)
            rows = cursor.fetchall()
            for row in rows:
                check = row
                if check is None:
                    return False  # return False if there is no such record
                else:
                    return True  # return True if there is record with this id

    def rework_data(self, worker_id, name, employees_position):  # create json
        worker_json = {
            "id": worker_id,
            "name": name,
            "position": employees_position
        }
        return worker_json


# add resource to API, specify path and start Flask.
api.add_resource(Workers, "/workers", "/workers/", "/workers/<int:id>")
if __name__ == '__main__':
    my_data = Database()
    connection = pymysql.connect(
        host=settings.host_name,
        user=settings.user_name,
        password=settings.user_password,
        database=settings.database,
        cursorclass=pymysql.cursors.DictCursor
    )
    app.run(debug=True)
