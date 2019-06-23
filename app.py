from flask import Flask
import random
import json

app = Flask(__name__)

USER_ID = "1"
promotion_text = "Скидка скидка 15%"

stepik_alive = True

workhours_opens = '10:00'
workhours_closes = '22:00'

meals = [{
    "title": "Chicken",
    "id": 1,
    "available": True,
    "picture": '',
    "price": 20.0,
    "category": 1
}, {
    "title": "Milk",
    "id": 2,
    "available": True,
    "picture": '',
    "price": 10.0,
    "category": 1
}]


@app.route("/")
def hello():
    return "<h1>" + "Test" + "</h1"


@app.route("/alive")
def alive():
    config_file = open('config.json', 'r', encoding="utf-8")
    config_content = config_file.read()
    data = json.loads(config_content)
    config_file.close()
    if stepik_alive == True:
        return json.dumps({"alive": data['alive']})


@app.route("/workhours")
def workours():
    config_file = open('config.json', 'r', encoding="utf-8")
    config_content = config_file.read()
    data = json.loads(config_content)
    config_file.close()

    return json.dumps(data["workhours"])
    # json.dumps({"opens": workhours_opens, "closes": workhours_closes})
    # '{"opens": "'+workhours_opens+'", "closes":"'+workhours_closes+'"}'


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0, 2)
    promotion_file = open("promotions.json", "r", encoding="utf-8")
    promotions = json.loads(promotion_file.read())
    return json.dumps(promotions[promotion_number], ensure_ascii=False)
    # '{"promotion":"'+promotions[random.randint(0,2)]+'"}'


@app.route("/promo/<code>")
def promo(code):
    promos_file = open("promo.json", "r", encoding="utf-8")
    promocodes = json.loads(promos_file.read())
    for promocode in promocodes:
        if promocode["code"] == code:
            users_file_r = open('users.json', 'r', encoding="utf-8")
            users_data = json.loads(users_file_r.read())
            users_file_r.close()

            users_data[USER_ID]['promocode'] = code

            users_file_w = open("users.json", "w", encoding="utf-8")
            users_file_w.write(json.dumps(users_data))
            users_file_w.close()

            return json.dumps({"valid": True, "discount": promocode['discount']}, ensure_ascii=False)
    return json.dumps({"valid": False})


@app.route("/meals")
def meals_route():
    users_file_r = open('users.json', 'r', encoding="utf-8")
    users_data = json.loads(users_file_r.read())
    users_file_r.close()

    discount=0
    promocode = users_data[USER_ID]["promocode"]
    if  promocode != None:
        promos_file = open("promo.json", "r", encoding="utf-8")
        promocodes = json.loads(promos_file.read())
        promos_file.close()
        for p in promocodes:
            if p["code"] == promocode:
                discount = p["discount"]
        for meal in meals:
            meal["price"]= (1-discount/100)*meal["price"]
    return json.dumps(meals)


app.run("0.0.0.0", 8000)
