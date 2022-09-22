from ast import Or
from flask import render_template, request, redirect, session
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import random
from flask_app.models.user_model import Accounts
from flask_app.models.order_model import Orders
from flask_app.models.favorite_model import Favorites
bcrypt = Bcrypt(app)
app.secret_key = "isaiah"

@app.route("/")
def index():
    return render_template("login_page.html")

@app.route("/home")
def home_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id':session['user_id']
    }
    one_user = Accounts.get_user(data)
    return render_template("home_page.html", users = one_user)

@app.route("/register_page")
def reg_page():
    return render_template("register_page.html")


@app.route("/register", methods=["POST"])
def register():
    data ={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'address':request.form['address'],
        'city':request.form['city'],
        'state':request.form['state'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    if not Accounts.validate_registration(request.form):
        return redirect("/")
    if not Accounts.validate_email(request.form):
        return redirect("/")
    user_id = Accounts.save(data)
    session['user_id']= user_id
    user = Accounts.get_user({"id": user_id})
    session['first_name'] = user.first_name
    return redirect("/home")


@app.route("/login", methods= ['POST'])
def login():
    user = Accounts.check_email(request.form['email'])
    if not user:

    #Todo generate flash message
        return redirect("/")
    else:
        if bcrypt.check_password_hash(user.password, request.form['password']) == True:
            session['user_id']= user.id
            print(session['user_id'])
            #user_login = Accounts.get_user({"id": user.id})
            session['first_name'] = user.first_name
            return redirect("/home")
        else:
            flash("Password does not match with email.")
            return redirect("/")

@app.route("/update_user_page/<int:id>")
def update_user_page(id):
    data ={
        'id':session['user_id']
    }
    one_user = Accounts.one_user(data)
    all_orders = Orders.get_all_closed(data)
    fav = Orders.get_fav(data)
    return render_template("edit_account.html", users= one_user, orders=all_orders, favorites = fav)

@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
    Accounts.update(request.form, id)
    return redirect("/home")

@app.route("/new_order_page")
def order_page():
    data ={
        'id':session['user_id']
    }
    one_user = Accounts.one_user(data)
    return render_template("new_order.html", users=one_user)

@app.route("/order", methods=["POST"])
def new_order():
    data ={
        'method':request.form['method'],
        'size':request.form['size'],
        'crust':request.form['crust'],
        'toppings':request.form['toppings'],
        'quantity':request.form['quantity'],
        'user_id':session['user_id'],
    }
    order = Orders.save(data)
    return redirect("/purchase_page")



@app.route("/purchase_page")
def purchase():
    data={
        'id':session["user_id"]
    }
    print(data)
    order = Orders.get_all_open(data)
    one_user = Accounts.one_user(data)
    return render_template("purchase_page.html", orders=order, users = one_user)

@app.route("/purchase_order")
def order_purchase():
    data={
        'id':session['user_id']
    }
    purchase = Orders.order_purchase(data)
    return render_template("order_confirmation.html") 

@app.route("/favorite", methods=["POST"])
def favorite_order():
    data={
        'user_id':session['user_id'],
        'order_id':request.form['order_id']
    }
    id = session['user_id']
    #one_user = Accounts.one_user(data)
    print('data', data)
    Favorites.favorite(data)
    return redirect(f'/update_user_page/{id}')

@app.route("/favorite_order")
def order():
    data ={
        'id':session["user_id"]
    }
    fav = Orders.get_fav(data)
    one_user = Accounts.one_user(data)
    print(data)
    return render_template("fav_orders.html", favorites = fav, users = one_user)

@app.route("/delete_account/<int:id>")
def delete(id):
    Accounts.delete(id)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

