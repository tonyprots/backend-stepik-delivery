from flask import Flask
from flask_cors import CORS
from flask import request
import random
import json
import uuid
import datetime

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


@app.route("/")
def hello():
    return "<h1>" + "Server is ON" + "</h1"


@app.route("/alive")
def alive():
    data = file_read('config.json')
    if stepik_alive:
        return json.dumps({"alive": data['alive']})


@app.route("/workhours")
def workours():
    data = file_read('config.json')
    return json.dumps(data["workhours"])


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0, 2)
    promotions = file_read('promotions.json')
    return json.dumps(promotions[promotion_number], ensure_ascii=False)


@app.route("/promo/<code>")
def promo(code):
    promocodes = file_read('promo.json')
    for promocode in promocodes:
        if promocode["code"] == code:
            users_data = file_read('users.json')
            users_data[USER_ID]['promocode'] = code
            file_write("users.json", users_data)
            return json.dumps({"valid": True, "discount": promocode['discount']}, ensure_ascii=False)
    return json.dumps({"valid": False})


@app.route("/meals")
def meals_route():
    meals = file_read('meal.json')
    users_data = file_read('users.json')
    discount = 0
    promocode = users_data[USER_ID]["promocode"]
    if promocode != None:
        promocodes = file_read('promo.json')
        for p in promocodes:
            if p["code"] == promocode:
                discount = p["discount"]
        for meal in meals:
            meal["price"] = (1 - discount / 100) * meal["price"]
    return json.dumps(meals)


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        pass
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
        meals_copy = json.loads(json.dumps(meals))
        for meal in meals_copy:
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
        print(order[key]["submit_time"])

        if (order[key]["submit_time"])<time_zero:
            time_zero=(order[key]["submit_time"])
            key_id = key
    return json.dumps({
            'id': order[key_id]["id"],
            'ordered': order[key_id]["submit_time"],
            'meals': order[key_id]["meals"],
            'summ': order[key_id]["sum"],
            'status': order[key_id]["status"]
        })

app.run("0.0.0.0", 8000)
