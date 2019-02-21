import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS
from modules.post_data_to_database import post_data

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname=thoughtworks_cafeteria user=admin")


@app.route('/')
def login_page():
    return render_template('creating_login_page.html')
@app.route('/')
def customer_page():
    return render_template('creating_customer_login.html')

@app.route('/menu_page')
def menu_page():
    return render_template('menu_page.html')

@app.route('/employee-login')
def employee_page():
    return render_template('creating_customer_login.html')


@app.route('/post-data', methods=['GET'])
def get_data():
    print(request)
    post_data(connection, request.form)
    return render_template('detail_page.html', shared=request.form)

@app.route('/creating_customer_login', methods=['POST'])
def post_data_request():
    print(request)
    post_data(connection, request.form)
    return render_template('detail_page.html', shared=request.form)



if __name__ == '__main__':
    app.run()
