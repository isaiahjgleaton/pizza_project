import re
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
db = "pizza_project"
app.secret_key = "isaiah"

class Orders:
    def __init__(self,data):
        self.id = data["id"]
        self.method = data["method"]
        self.size = data["size"]
        self.crust = data["crust"]
        self.quantity = data["quantity"]
        self.toppings = data["toppings"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.open_order = data["open_order"]
        self.user_favorite = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO orders(method, size, crust, quantity, toppings, user_id) values(%(method)s, %(size)s, %(crust)s, %(quantity)s, %(toppings)s, %(user_id)s);"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def get_all_open(cls,data):
        query = "SELECT * FROM users JOIN orders ON orders.user_id = users.id WHERE users.id = %(id)s and open_order = True"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        orders = []
        for order in results:
            one_order = cls(order)
            data ={
                "id":order["user_id"],
                "method":order["method"],
                "size":order["size"],
                "crust":order["crust"],
                "toppings":order['toppings'],
                "quantity":order['quantity'],
                "created_at":order["created_at"],
                "updated_at":order["updated_at"]
            }
            #orders.user = Users(data)
            orders.append(one_order)
        return orders

    @classmethod
    def get_all_closed(cls,data):
        query = "SELECT * FROM orders LEFT JOIN users ON orders.user_id = users.id WHERE users.id = %(id)s and open_order = False"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        orders = []
        for order in results:
            one_order = cls(order)
            data ={
                "id":order["id"],
                "method":order["method"],
                "size":order["size"],
                "crust":order["crust"],
                "toppings":order['toppings'],
                "quantity":order['quantity'],
                "created_at":order["created_at"],
                "updated_at":order["updated_at"]
            }
            #orders.user = Users(data)
            orders.append(one_order)
        return orders

    @classmethod
    def order_purchase(cls,data):
        query = "UPDATE orders set open_order = False where user_id = %(id)s"
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_fav(cls,data):
        query = "SELECT * FROM orders left join favorites on favorites.order_id = orders.id WHERE favorites.user_id = %(id)s; "
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        orders = []
        for order in results:
            one_order = cls(order)
           
            orders.append(one_order)
        return orders