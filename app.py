from flask import Flask
import random
import json
app = Flask(__name__)

promotion_text = "Скидка скидка 15%"

stepik_alive = True

workhours_opens = '10:00'
workhours_closes = '22:00'

promocodes =[
    {"code":"doubletrouble","discount":50},
    {"code": "illbeback", "discount": 25},
    {"code":"stepik", "discount":25},
    {"code":"pleaseplease","discount":5},
    {"code":"libertyordeath", "discount":100}
    {"code": "summer", "discount": 10}
]

promotions = [
    "Скидка 15% по промокоду STEPIK",
    "Скидка 10% по промокоду SUMMER",
    "Удваиваем все пиццы по промокоду udodopizza"
]

meals = [{
"title":"Chicken",
"id":1,
"available":True,
"picture":'',
"price":20.0,
"category":1
}, {
"title":"Milk",
"id":2,
"available":True,
"picture":'',
"price":10.0,
"category":1
}]

@app.route("/")
def hello():
    return "<h1>" +"Test" +"</h1"


@app.route("/alive")
def alive():
    if stepik_alive==True:
        return'{"alive":true}'

@app.route("/workhours")
def workours():
    return '{"opens": "'+workhours_opens+'", "closes":"'+workhours_closes+'"}'

@app.route("/promo")
def promotion():
    return '{"promotion":"'+promotions[random.randint(0,2)]+'"}'

@app.route("/promo/<code>")
def promo(code):
    for promocode in promocodes:
        if promocode["code"] == code:
            return json.dumps({"valid":True,"discount":promocode['discount']})
    return json.dumps({"valid": False})

@app.route("/meals")
def meals_route():
    return json.dumps(meals)

app.run("0.0.0.0",8000)