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


@app.route('/backbutton')
def back_button_vendor():
    return render_template('welcome_page.html')


@app.route('/cancelbutton')
def cancel_button_for_vendor():
    return render_template('vendor_login_pag.html')


@app.route('/cancelbtn')
def cancel_btn_for_customer():
    return render_template('welcome_page.html')


@app.route("/backbtn")
def back_btn_available_and_report():
    return render_template('welcome_page.html')


@app.route("/menu_page_back_button")
def menu_page_back_button():
    return render_template('customer_login_page.html')


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


@app.route('/employee', methods=['POST'])
def menu_pages_requested():
    return post_data_customer(connection, request.form)


# @app.route('/vendor')
# def hot_items():
#     rows = database_selected_hot_items()
#     items = []
#     for row in rows:
#         items.append(row[0])
#     return render_template("jinja_cold.html", items=items)
#
#
# def database_selected_hot_items():
#     cursor = connection.cursor()
#     cursor.execute("select  item_name from item_menu where ref_id ='222'")
#     record = cursor.fetchall()
#
#     return record


# @app.route('/menu_page_for_cold_items')
# def display_available_cold_items():
#     return render_template('list_of_fruits.html')


@app.route('/vendor_page')
def vendor_page_login():
    return render_template('vendor_login_pag.html')


@app.route('/juice_world')
def juice_login():
    return render_template("vendor_login_page.html", name='111')


@app.route('/madras_cafe')
def hot_login():
    return render_template("vendor_login_page.html", name='222')


@app.route('/vendor_login', methods=['POST'])
def vendor_login_pages_requested():
    return post_data_vendor(connection, request.form)


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
    returned = (int(request.query_string.decode().split('=')[1]),)
    lists = list(returned)
    index = lists[0]
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("vendor_menu.html", items=items, name=index)


def database_selected_cold_items(connection, user_data):
    cursor = connection.cursor()
    query = "select  item_name from items_menu where ref_id =%s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()

    return record


@app.route('/submission', methods=['POST'])
def list_of_all_cold_item():
    return set_list_of_item_in_database(connection, request.form)


def set_list_of_item_in_database(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    sql_update = "update items_menu set availability = 'no' where ref_id=%(vendor_id)s"
    # cursor.execute(sql_update, (int(user_data.decode().split('=')[1]),))
    sql_data = "update items_menu set availability = 'yes' WHERE item_name  IN %s"
    cursor.execute(sql_update, {'vendor_id': array_value})
    cursor.execute(sql_data, (array,))
    connection.commit()
    cursor.close()


@app.route('/beverage_for_hot', )
def hot_items():
    rows = database_selected_hot_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("available_hot.html", items=items)


def database_selected_hot_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from items_menu where availability  ='yes' ")
    record = cursor.fetchall()

    return record


@app.route('/report_generation')
def calculation_madras_coffee():
    sum = calculation_hot()
    return render_template("display_report.html", items=sum)


def calculation_hot():
    cursor = connection.cursor()
    cursor.execute(
        "select sum(cost*quantity)from items_menu inner join shopping_cart on items_menu.item_id = shopping_cart.item_id where ref_id = 222;")
    cost = cursor.fetchall()
    cursor.close()
    return cost


# @app.route('/beverage_for_cold', )
# def cold_items():
#     rows = database_selected_avail_cold_items()
#     items = []
#     for row in rows:
#         items.append(row[0])
#     return render_template("available_cold.html", items=items)
#
#
# def database_selected_avail_cold_items():
#     cursor = connection.cursor()
#     cursor.execute("select  item_name from item_menu where availability  ='yes'")
#     record = cursor.fetchall()
#
#     return record


# @app.route('/menu_page_for_hot_items', methods=['POST'])
# def list_of_all_hot_items():
#     return set_list_of_hot_item(connection, request.form)
#
#
# def set_list_of_hot_item(connection, user_data):
#     cursor = connection.cursor()
#     query = "select item_id from item_menu where item_name=%(item)s", {'item': user_data['item']}
#     cursor.fetchall(query)
#     insert = "insert into cart_details values where item_id cursor = connection.cursor()=%(query)s"
#     cursor.execute(insert)
#     cursor.close()
#
#
# @app.route('/menu_page_for_cold_items', methods=['POST'])
# def list_of_all_cold_items():
#     return set_list_of_cold_item(connection, request.form)
#
#
# def set_list_of_cold_item(connection, user_data):
#     cursor = connection.cursor()
#     query = "select item_id from item_menu where item_name=%(item)s", {'item': user_data['item']}
#     cursor.fetchall(query)
#     insert = "insert into cart_details values where item_id cursor = connection.cursor()=%(query)s"
#     cursor.execute(insert)
#     cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
