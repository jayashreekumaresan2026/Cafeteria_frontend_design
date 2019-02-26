import psycopg2
from flask import Flask, render_template, request

from app import connection

app = Flask(__name__)


@app.route('/')
def cold():
    rows = database_connection_cold()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold.html", items=items)


@app.route('/submission', methods=['POST'])
def menu_list_cold():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    d = dict(user_data)
    for key in d:
        cursor.execute("update menu_item set available = 1  where item_name= value(%s); ", (print(key),))
    connection.commit()
    cursor.close()


def database_connection_cold():
    print("try is running")
    connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                  database="thoughtworks_cafeteria")
    cursor = connection.cursor()
    cursor.execute("select  item_name from menu_item where ref_id= 'cb1'")
    record = cursor.fetchall()

    return record


if __name__ == '__main__':
    app.run()
