from flask import Flask
import random
import json

app = Flask(__name__)

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

app.run("0.0.0.0", 8000)