import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = thoughtworks_cafeteria user=admin")


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/backbutton')
def back_button_for_vendor():
    return render_template('welcome_page.html')


@app.route('/cancelbutton')
def cancel_button_for_vendor():
    return render_template('vendor_menu_page.html')


@app.route('/cancelbtn')
def cancel_btn_for_customer():
    return render_template('welcome_page.html')


@app.route("/backbtn")
def back_buttton_for_available_and_report():
    return render_template('welcome_page.html')


@app.route("/menu_page_back_button")
def customer_menu_page_back_button():
    return render_template('customer_login_page.html')


@app.route("/back_from_available_page")
def vendor_menu_back_button_from_checklist():
    return render_template('vendor_items_availability_and_report_button.html')


@app.route('/customer_page')
def customer_page_login():
    return render_template('customer_login_page.html')


# def post_data(connection, user_data):
#     cursor = connection.cursor()
#     cursor.execute("""insert into shopping_cart (employee_id) values (%s);""",
#                    {'employee_id': user_data['id']}, )
#     connection.commit()
#     cursor.close()


def validate_customer_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(emp_id)s ",
                   {'emp_id': user_data['id']}, )
    returned_rows = cursor.fetchall()
    cursor.close()

    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        # post_data(connection, user_data)
        return render_template('customer_menu_page.html')


@app.route('/customer_login_page', methods=['POST'])
def menu_pages_for_customer():
    return validate_customer_data(connection, request.form)


@app.route('/vendor_page')
def vendor_page_login():
    return render_template('vendor_menu_page.html')


@app.route('/available_hot_items')
def render_to_hot_menu():
    return render_template('available_hot_items.html')


@app.route('/available_cold_items')
def render_to_cold_menu():
    return render_template('available_cold_items.html')


@app.route('/hai', )
def render():
    return render_template('hai.html')


@app.route('/menu_page_for_cold_items', methods=['POST'])
def cart_data():
    return post_cart_data(connection, request.form)

def post_cart_data(connection, update_data):
    value = update_data.to_dict()
    a = []
    b = []
    a.append(list(value.keys())[0])
    b.append(list(value.values())[1])
    cursor = connection.cursor()
    query = "insert into cart_details (item_id,quantity) select item_id, {} from item where item_name = '{}'".format(b[0], a[0])
    cursor.execute(query)
    connection.commit()
    cursor.close()
    return query




@app.route('/juice_world_for_vendor')
def juice_login_for_vendor():
    return render_template("vendor_login_page.html", name='111')


@app.route('/madras_cafe_for_vendor')
def hot_login_for_vendor():
    return render_template("vendor_login_page.html", name='222')


@app.route('/vendor_login_page', methods=['POST'])
def vendor_login_page_requested():
    return validation_for_vendor(connection, request.form)


def validation_for_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute(
        "select vendor_id,vendor_password  from vendor_detail where (vendor_id = %(vendor_id)s AND vendor_password=%(vendor_password)s )",
        {'vendor_id': user_data['id'], 'vendor_password': user_data['psw']}, )

    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:

        return render_template('vendor_items_availability_and_report_button.html', vendorname=user_data['vendorname'])


@app.route('/available_item_and_report_button')
def cold_item_check_availability():
    rows = selected_cold_items_in_the_database(connection, request.query_string)
    returned = (int(request.query_string.decode().split('=')[1]),)
    lists = list(returned)
    index = lists[0]
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("vendor_availability_page.html", items=items, name=index)


def selected_cold_items_in_the_database(connection, user_data):
    cursor = connection.cursor()
    query = "select  item_name from item where id =%s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()

    return record


@app.route('/submission', methods=['POST'])
def list_of_all_item():
    rows = set_list_of_item_in_database(connection, request.form)
    return render_template('welcome_page.html', item=rows)


def set_list_of_item_in_database(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    sql_update = "update item set is_available = 'no' where id=%(vendor_id)s"
    sql_data = "update item set is_available = 'yes' WHERE item_name  IN %s"
    cursor.execute(sql_update, {'vendor_id': array_value})
    cursor.execute(sql_data, (array,))
    connection.commit()
    cursor.close()


@app.route('/beverage_for_cold', )
def hot_items():
    rows = database_selected_hot_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("available_cold_items.html", items=items)


def database_selected_hot_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from item where is_available  ='yes' AND id=111 ")
    record = cursor.fetchall()

    return record


@app.route('/beverage_for_hot', )
def cold_items():
    rows = database_selected_avail_cold_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("available_hot_items.html", items=items)


def database_selected_avail_cold_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from item where is_available  ='yes' AND id=222")
    record = cursor.fetchall()

    return record


@app.route('/report_generation')
def calculation_madras_coffee():
    sum = calculation_hot()
    return render_template("display_report.html", items=sum)


def calculation_hot():
    cursor = connection.cursor()
    cursor.execute(
        "select sum(cost*quantity)from item inner join order_details on item.item_id = order_details.item_id where id = 222;")
    cost = cursor.fetchall()
    cursor.close()
    return cost


if __name__ == '__main__':
    app.run(debug=True)
