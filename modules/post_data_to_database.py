def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into employee(name, employee_id) values(%s, %s);""",
                   (user_data['name'], user_data['id']))
    connection.commit()
    cursor.close()