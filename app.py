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


def validate_customer_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(emp_id)s ",
                   {'emp_id': user_data['id']}, )
    returned_rows = cursor.fetchall()
    cursor.close()

    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        return render_template('customer_menu_page.html', item=user_data['id'])


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


@app.route('/menu_page_for_cold_items', methods=['POST'])
def update_item_for_cold():
    rows = update_database_cold_items(connection, request.form)
    return render_template('welcome_page.html', item=rows)


def update_database_cold_items(connection, update_data):
    item = update_data.to_dict()
    a = []
    b = []
    c = []
    i = 1
    j = 2
    index = 0
    if i != len(item):
        for row in range(len(item)):
            a.append(list(item.keys())[i])
            b.append(list(item.values())[j])
            c.append(list(item.values())[0])
            cursor = connection.cursor()
            update_details = "insert into order_detail(item_id,quantity,employee_id) select item_id,{},{} from item where item_name='{}'".format(
                b[index], c[0], a[index])
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
            i += 2
            j += 2
            index += 1
    return update_details


@app.route('/menu_page_for_hot_items', methods=['POST'])
def update_item_for_hot():
    rows = update_database_hot_items(connection, request.form)
    return render_template('welcome_page.html', item=rows)


def update_database_hot_items(connection, update_data):
    item = update_data.to_dict()
    a = []
    b = []
    c = []
    i = 1
    j = 2
    index = 0
    if i != len(item):
        for row in range(len(item)):
            a.append(list(item.keys())[i])
            b.append(list(item.values())[j])
            c.append(list(item.values())[0])
            cursor = connection.cursor()
            update_details = "insert into order_detail(item_id,quantity,employee_id) select item_id,{},{} from item where item_name='{}'".format(
                b[index], c[0], a[index])
            cursor.execute(update_details)
            connection.commit()
            cursor.close()
            i += 2
            j += 2
            index += 1
    return update_details


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


@app.route('/available_item_button')
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


@app.route('/beverage_for_cold', methods=['POST'])
def all_hot_item():
    return cold_item(connection, request.form)


def cold_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = database_selected_hot_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("available_cold_items.html", items=items, empid=array_value)


def database_selected_hot_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from item where is_available  ='yes' AND id=111 ")
    record = cursor.fetchall()

    return record


@app.route('/beverage_for_hot', methods=['POST'])
def all_cold_item():
    return hot_items(connection, request.form)


def hot_items(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = database_selected_avail_cold_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("available_hot_items.html", items=items, empid=array_value)


def database_selected_avail_cold_items():
    cursor = connection.cursor()
    cursor.execute("select  item_name from item where is_available  ='yes' AND id=222")
    record = cursor.fetchall()

    return record


@app.route('/report_generation_button', methods=['POST'])
def calculation_for_report():
    report_table= calculation(connection, request.form)
    totalcost = total_cost(connection, request.form)
    sum_cost = tuple(report_table)

    return render_template("display_report.html", item=totalcost, items=sum_cost)


def calculation(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]

    sql_update = "select employee_id,id,item_name,(quantity*cost),date from item inner join order_detail on item.item_id = order_detail.item_id where id = %(vendor_id)s"
    cursor.execute(sql_update, {'vendor_id': array_value})
    report_table = cursor.fetchall()
    cursor.close()
    return report_table


def total_cost(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]

    sql_query = "select sum(quantity*cost) from item inner join order_detail on item.item_id = order_detail.item_id where id = %(vendor_id)s"
    cursor.execute(sql_query, {'vendor_id': array_value})
    totalcost = cursor.fetchall()
    cursor.close()
    return totalcost


if __name__ == '__main__':
    app.run(debug=True)
