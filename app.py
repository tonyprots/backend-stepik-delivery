from flask import Flask
from flask_cors import CORS
from flask import request
import random
import json
import uuid
import datetime
import sqlite3
import os
import urllib
import requests

from twilio.rest import Client


app = Flask(__name__)
CORS(app)

USER_ID = "1"
stepik_alive = True


def file_read(file):
    read_file = open(file, 'r', encoding="utf-8")
    file_content = read_file.read()
    data = json.loads(file_content)
    read_file.close()
    return data


def file_write(file, data):
    write_file = open(file, "w", encoding="utf-8")
    write_file.write(json.dumps(data))
    write_file.close()


def get_cursor():
    connection = sqlite3.connect("database.db")
    c = connection.cursor()
    return c

def fill_database():
    api_key = "3ac8a2f6a0112783867a41e3858e1c26"
    key_words = "cake"
    c = get_cursor()

    for page in range(1,4):
        params = {"key": api_key, "q":key_words, "page": page}
        url_string = "https://www.food2fork.com/api/search?" + urllib.parse.urlencode(params)
        r = requests.get(url_string)
        data = r.json()
        for item in data["recipes"]:
            c.execute("""
            INSERT INTO meals (title, available, picture, price, category) VALUES (?,?,?,?,?)
            """,[
                item["title"],
                1,
                item["image_url"],
                item["social_rank"] + random.randint(0,100),
                1
            ])
            c.connection.commit()
    c.connection.close()



def init_db():
    c = get_cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        title text,
        available integer,
        picture text,
        price real,
        category integer
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS promocodes (
        id integer PRIMARY KEY,
        code text,
        discount real
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        promocode text
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id integer PRIMARY KEY,
        ordered text,
        meals
    )
    """)

    c.execute("""
    INSERT INTO meals VALUES (1, "Chicken", 1, "", 20.0, 1)
    """)

    c.execute("""
    INSERT INTO meals VALUES (2, "Milk", 1, "", 10.0, 1)
    """)

    c.execute("""
    INSERT INTO promocodes VALUES(1, "stepik", 30.0)
    """)
    c.execute("""
    INSERT INTO promocodes VALUES(2, "delivery", 10.0)
    """)

    c.execute("""
    INSERT INTO users VALUES(1, null)
    """)

    c.connection.commit()
    c.connection.close()


@app.route("/")
def hello():
    return "<h1>" + "Server is ON" + "</h1"


@app.route("/alive")
def alive():
    data = file_read('config.json')
    return json.dumps({"alive": data['alive']})


@app.route("/workhours")
def workours():
    data = file_read('config.json')
    return json.dumps(data["workhours"])

@app.route("/promo/<code>")
def promo(code):
    c = get_cursor()
    c.execute("""
    SELECT * FROM promocodes WHERE code = ?
    """, [code])
    result = c.fetchone()
    if result is None:
        return json.dumps({"valid": False})

    promo_id, promo_code, promo_discount = result
    c.execute("""
    UPDATE users
    SET promocode = ?
    WHERE id = ?
    """, (promo_code, int(USER_ID)))
    c.connection.commit()
    c.connection.close()
    return json.dumps({"valid": True, "discount": promo_discount})


@app.route("/meals")
def meals_route():
    c = get_cursor()
    c.execute("""
        SELECT discount
        FROM promocodes
        WHERE code = (
            SELECT promocode
            FROM users
            WHERE id = ?
        ) 
        """, (int(USER_ID),))
    discount = 0
    result = c.fetchone()
    if result is not None:
        discount = result[0]
    meals = []
    for meals_info in c.execute("SELECT * FROM meals"):
        meals_id, title, available, picture, price, category = meals_info
        meals.append({
            "id": meals_id,
            "title": title,
            "available": bool(available),
            "picture": picture,
            "price": price * (1.0 - discount / 100),
            "category": category
        })
    return json.dumps(meals)


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        orders = file_read("orders.json")
        return json.dumps(orders)
    elif request.method == "POST":
        discount = 0
        raw_data = request.data.decode("utf-8")
        data = json.loads(raw_data)
        meals = file_read('meal.json')
        users_data = file_read('users.json')
        promocode = users_data[USER_ID]['promocode']
        if promocode != None:
            promocodes = file_read('promo.json')
            for p in promocodes:
                if p["code"] == promocode:
                    discount = p["discount"]
        sum = 0
        for meal in meals:
            meal_id = meal['id']
            for user_meal_id in data['meals']:
                if user_meal_id == meal_id:
                    sum += (1 - discount / 100) * meal["price"]
                    break
        new_order_id = str(uuid.uuid4())
        new_order = {
            "id": new_order_id,
            "submit_time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "meals": data["meals"],
            "sum": sum,
            "status": "accepted",
            "user_id": USER_ID
        }
        order_data = file_read('orders.json')
        order_data[new_order_id] = new_order
        file_write('orders.json', order_data)

        return json.dumps({"order_id": new_order_id, "status": new_order['status']})


@app.route("/activeorder")
def activeorders():
    order = file_read("orders.json")
    time_zero = "25-10-2019 00:27"
    key_id = "0"
    for key in order:
        if (order[key]["submit_time"]) < time_zero:
            time_zero = (order[key]["submit_time"])
            key_id = key
    return json.dumps({
        'id': order[key_id]["id"],
        'ordered': order[key_id]["submit_time"],
        'meals': order[key_id]["meals"],
        'summ': order[key_id]["sum"],
        'status': order[key_id]["status"]
    })


@app.route("/order/<id>", methods=["DELETE"])
def delete(id):
    order = file_read('orders.json')
    order[id]['status'] = "CANCELLED"
    file_write('orders.json', order)
    return json.dumps({"status": True})

@app.route("/notification")

# Сюда бы внести номер юзера и инфу о заказе. Было бы круто перенести в создание заказа.
def notif():
    sms_client = Client(
        "ACb7585a47107a1adb0829f7cd5c040eb0",
        "deaff95b749290eb0b3307eec79ddd8b"
    )
    message = sms_client.messages.create(
        body = "New order is accepted!",
        from_= "+19255264119",
        to = "+79119782904"
    )

    return json.dumps({"status":True})




if not os.path.exists("database.db"):
    init_db()
    fill_database()

app.run("0.0.0.0", 9000)
