import re
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
db = "pizza_project"
app.secret_key = "isaiah"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Accounts:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = MySQLConnection(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users(first_name, last_name, email, address, city, state, password) values(%(first_name)s, %(last_name)s, %(email)s, %(address)s, %(city)s, %(state)s, %(password)s);"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def one_user(cls, id):
        query = "SELECT * FROM users where id=%(id)s"
        results = MySQLConnection(db).query_db(query,id)
        #print(data)
        return cls(results[0])

    @classmethod
    def update(cls, data, id):
        query = f"UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, address=%(address)s, city=%(city)s, state=%(state)s where id = {id}"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        return True
    
    @classmethod
    def delete(cls,id):
        query = f"DELETE FROM users where id = {id}"
        results = MySQLConnection(db).query_db(query)
        return results
        
    @staticmethod
    def validate_registration(users):
        is_valid = True
        if len(users['first_name']) < 2:
            flash("name must be longer then 2 characters")
            is_valid = False
        if len(users['last_name']) < 2:
            flash("name must be longer then 2 characters")
            is_valid = False
        if len(users['password']) < 8:
            flash("password must be longer then 8 characters")
            is_valid = False
        if users['password'] != users["password_confirm"]:
            flash("passwords do not match")
            is_valid = False
        
        return is_valid
    @staticmethod
    def validate_email(users):
        is_valid = True
        if not EMAIL_REGEX.match(users['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
    @classmethod
    def check_email(cls,email):
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = MySQLConnection(db).query_db(query, {'email': email})
        if len(results) < 1:
            flash("Email does not exist")
            return None
        return cls(results[0])