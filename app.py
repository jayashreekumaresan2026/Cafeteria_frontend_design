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


@app.route('/vendor_page')
def vendor_page_login():
    return render_template('vendor_login_page.html')


# inserting data into the database while user id is valid
def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into customer_details(employee_id ) values(%s);""",
                   (user_data['id'],))
    connection.commit()
    cursor.close()


# checking validation for the employee to move further process
def post_data_customer(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id = %(emp_id)s ",
                   {'emp_id': user_data['id']})
    returned_rows = cursor.fetchall()
    cursor.close()

    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        post_data(connection, user_data)
        return render_template('menu_page.html')


@app.route('/employee', methods=['POST'])
def menu_pages_requested():
    return post_data_customer(connection, request.form)


def post_data_vendor(connection, vendor_data):
    cursor = connection.cursor()
    cursor.execute(
        "select vendor_id,vendor_password from vendor_details where vendor_id = %(vendor_id)s AND vendor_password=%(vendor_password)s",
        {'vendor_id': vendor_data['id']}, {'vendor_password': vendor_data['psw']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_items_availability_and_report.html')
    else:
        return render_template('menu_page.html')


@app.route('/vendor_login', methods=['POST'])
def item_pages_requested():
    return post_data_vendor(connection, request.form)


if __name__ == '__main__':
    app.run()
