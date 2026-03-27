from flask import request

# In-memory dictionary to replace the broken MongoDB cluster
users_db = {}

def insert_data():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        password = request.form.get('pass', '')

        if email not in users_db:
            users_db[email] = {
                'name': name,
                'email': email,
                'password': password
            }
            return True
        else:
            return False
    return False

def check_user():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('pass', '')

        user_data = users_db.get(email)
        if user_data is None or user_data['password'] != password:
            return False, ""
        else:
            return True, user_data["name"]
    return False, ""