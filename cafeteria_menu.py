import psycopg2
from flask import Flask, render_template, request

from app import connection

app = Flask(__name__)

connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                              database="thoughtworks_cafeteria")


@app.route('/beverage_for_cold')
def cold_items():
    rows = database_connection_cold()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold.html", items=items)

@app.route('/')
def show_items_to_menu():
    rows = database_connection_display()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_menu.html", items=items)


@app.route('/submission', methods=['POST'])
def menu_list_cold():
    return database_connection_list_cold(connection, request.form)


def database_connection_list_cold(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_data = "update menu_item set available = 10 WHERE item_name  IN %s"
    cursor.execute(sql_data, (array,))
    connection.commit()
    cursor.close()


def database_connection_display():
    cursor = connection.cursor()
    cursor.execute("select  item_name from menu_item where available= 10")
    record_data = cursor.fetchall()

    return record_data


def database_connection_cold():
    cursor = connection.cursor()
    cursor.execute("select  item_name from menu_item where ref_id= 'cb1'")
    record = cursor.fetchall()

    return record


if __name__ == '__main__':
    app.run()
