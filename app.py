import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS
from modules.post_data_to_database import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=admin")

#--connection for the welcome page

@app.route('/')
def login_page():
    return render_template('creating_login_page.html')

#connection for the customer login page
@app.route('/customer_page')
def customer_page():
    return render_template('creating_customer_login.html')

#checking the user_id within the database and navigate the the menu page
@app.route('/employee', methods=['POST'])
def menu_page():
    post_data(connection, request.form)
    return render_template('menu_page.html', shared=request.form)

#connection for the juice item page
@app.route('/juice_bevarage')
def list_of_fruits():
    return render_template('add_cart_fruits.html')

#connection for the menu hot item page
@app.route ('/hot_bevarage')
def list_of_hots():
    return render_template('add_cart_for_hot.html')

#checking the vendor login within the database
@app.route ('/menu_page', methods=['POST'])
def get_vendor_data():
    post_data(connection, request.form)
    return render_template('vendor_items_availability_and_report.html', shared=request.form)

#get the ordered items from cart
@app.route('/juice_beverage')
def get_order_item_for_juice():
    post_data(connection, request.form)
    return render_template('final_page.html', shared=request.form)

#get the ordered  items from cart
def get_order_item_for_hot():
    post_data(connection, request.form)
    return render_template('final_page.html', shared=request.form)

if __name__ == '__main__':
    app.run()
