import re
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
db = "pizza_project"
app.secret_key = "isaiah"

class Favorites:
    def __init__(self,data):
        self.user_id = data['user_id']
        self.order_id = data['order_id']

    @classmethod
    def favorite(cls,data):
        query = "INSERT INTO favorites(user_id, order_id) values(%(user_id)s, %(order_id)s);"
        results = MySQLConnection(db).query_db(query, data)
        print('query', query)
        print('results', results)
        return results

    @classmethod
    def get_fav(cls,data):
        query = "SELECT * FROM favorites left join orders on favorites.order_id = orders.id WHERE favorites.user_id = %(id)s; "
        results = MySQLConnection(db).query_db(query,data)
        print(results)
        orders = []
        for order in results:
            one_order = cls(order)
            data ={
                'id':order['user_id'],
                'order_id':order['order_id']
            }
            orders.append(one_order)
        return orders
