#
# #storing  the user data in the  the database
#
# def post_data_for_user(connection, user_data):
#     cursor = connection.cursor()
#     cursor.execute("""insert into employee(vendor_id, vendor_name,vendor_password) values(%s, %s, %s);""",
#                    (user_data['id'] ))
#     connection.commit()
#     cursor.close()
#
#
# #storing  the vendor data in the  the database
# def post_data_for_vendor(connection, vendor_data):
#     cursor = connection.cursor()
#     cursor.execute("""insert into employee(vendor_id, vendor_name,vendor_password) values(%s, %s, %s);""",
#                    (vendor_data['name'], vendor_data['id'],vendor_data['password']))
#     connection.commit()
#     cursor.close()
#
# # validating the vendor data with the database
# def post_data(connection, user_data):
#
#     cursor = connection.cursor()
#     cursor.execute("""select employee_id from employee_details where employee_id = %s ;""", (user_data['user_id'],))
#     connection.commit()
#     cursor.close()
#
#
#
#
#
def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee_details(employee_id) values(%s);""",
                   (user_data['id'] ))
    connection.commit()
    cursor.close()
