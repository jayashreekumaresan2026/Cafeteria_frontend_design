import psycopg2
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    row = database_connect()
    return render_template("jinja.html", items=row)


def database_connect():
    try:
        print("try is running")
        connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                      database="thoughtworks_cafeteria")
        cursor = connection.cursor()
        cursor.execute("select  item_name from menu_item where ref_id= 'cb1'")
        record = cursor.fetchall()

        return record


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run()
