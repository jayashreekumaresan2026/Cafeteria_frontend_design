def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee1(emp_id) values(%s);""",
                   ( user_data['emp_id']))
    connection.commit()
    cursor.close()
