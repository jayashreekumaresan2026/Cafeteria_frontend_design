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


@app.route('/vendor')
def hot_items():
    rows = database_selected_hot_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold.html", items=items)


def database_selected_hot_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from item_menu where ref_id ='222'")
    record = cursor.fetchall()

    return record


@app.route('/menu_page_for_cold_items')
def display_available_cold_items():
    return render_template('list_of_fruits.html')


@app.route('/employee', methods=['POST'])
def menu_pages_requested():
    return post_data_customer(connection, request.form)


# checking validation for the employee to move further process
def post_data_customer(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(emp_id)s ",
                   {'emp_id': user_data['id']}, )
    returned_rows = cursor.fetchall()
    cursor.close()

    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        return render_template('menu_page.html')


@app.route('/vendor_page')
def vendor_page_login():
    return render_template('vendor_login_pag.html')


@app.route('/vendor_login', methods=['POST'])
def vendor_login_pages_requested():
    return post_data_vendor(connection, request.form)


@app.route('/juice_world')
def juice_login():
    return render_template("vendor_login_page.html", name='111')


@app.route('/madras_cafe')
def hot_login():
    return render_template("vendor_login_page.html", name='222')


def post_data_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(
        "select vendor_id,vendor_password  from vendor_detail where (vendor_id = %(vendor_id)s AND vendor_password=%(vendor_password)s )",
        {'vendor_id': user_data['id'], 'vendor_password': user_data['psw']}, )

    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:

        return render_template('vendor_items_availability_and_report.html', vendorname=user_data['vendorname'])


@app.route('/available_item')
def cold_item():
    rows = database_selected_cold_items(connection, request.query_string)
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("jinja_cold.html", items=items)


def database_selected_cold_items(connection, user_data):
    cursor = connection.cursor()
    query = "select  item_name from item_menu where ref_id =%s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()

    return record


@app.route('/submission', methods=['POST'])
def list_of_all_cold_items():
    return set_list_of_in_database(connection, request.form)


def set_list_of_in_database(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    sql_update = "update item_menu set availability = 'no'"
    sql_data = "update item_menu set availability = 'yes' WHERE item_name  IN %s"
    cursor.execute(sql_update)
    cursor.execute(sql_data, (array,))
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    app.run()
