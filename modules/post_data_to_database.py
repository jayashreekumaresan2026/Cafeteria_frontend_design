def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""select employee_id from employee_details where employee_id = %s ;""", (user_data['user_id'],))

    connection.commit()
    cursor.close()
