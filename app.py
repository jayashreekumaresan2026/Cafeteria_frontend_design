import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = thoughtworks_cafeteria user=admin")


# --connection for the welcome page status

@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


# connection for the customer login page
@app.route('/customer_page')
def customer_page_login():
    return render_template('customer_login_page.html')


@app.route('/beverage_for_cold')
def list_of_juices():
    return render_template('list_of_fruits.html')


@app.route('/beverage_for_hot')
def list_of_hots():
    return render_template('list_of_hot.html')


# checking validation for the employee to move further process
def post_data_customer(connection, data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(emp_id)s ",
                   {'emp_id': data['id']}, )
    returned_rows = cursor.fetchall()
    cursor.close()

    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        return render_template('menu_page.html')


@app.route('/employee', methods=['POST'])
def menu_pages_requested():
    return post_data_customer(connection, request.form)


@app.route('/vendor_page')
def vendor_page_login():
    return render_template('vendor_login_page.html')


@app.route('/vendor_login', methods=['POST'])
def item_pages_requested():
    return post_data_vendor(connection, request.form)


def post_data_vendor(connection, vendor_data):
    cursor = connection.cursor()
    cursor.execute(
        "select vendor_id  from vendor_details where vendor_password = %(vendor_id)s ",
        {'vendor_id': vendor_data['id']}, )

    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        return render_template('jinja_cold.html')


@app.route('/beverage_for_cold')
def cold_items():
    rows = database_selected_cold_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold.html", items=items)


@app.route('/submission', methods=['POST'])
def menu_list_cold():
    return database_connection_list_cold(connection, request.form)


@app.route('/beverage_for_hot' )
def show_items_to_menu():
    rows = database_connection_display()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_menu.html", items=items)


def database_selected_cold_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from menu_item where ref_id= 'cb1'")
    record = cursor.fetchall()

    return record


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


if __name__ == '__main__':
    app.run()
