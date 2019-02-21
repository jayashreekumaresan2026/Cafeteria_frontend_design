
#validating the user data with the database

def post_data(connection, user_data):

    cursor = connection.cursor()
    cursor.execute("""select employee_id from employee_details where employee_id = %s ;""", (user_data['user_id'],))
    connection.commit()
    cursor.close()


# validating the vendor data with the database
def post_data_for_vendor(connection, vendor_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee(vendor_id, vendor_name,vendor_password) values(%s, %s, %s);""",
                   (vendor_data['name'], vendor_data['id'],vendor_data['password']))
    connection.commit()
    cursor.close()

