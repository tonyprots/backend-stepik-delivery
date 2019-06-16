from flask import Flask
app = Flask(__name__)

promotion_text = "Скидка скидка 15%"

stepik_alive = True

workhours_opens = '10:00'
workhours_closes = '22:00'

promocode ="stepik"


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

@app.route("/promotion")
def promotion():
    return '{"promotion":"'+promotion_text+'"}'

@app.route("/promo/<code>")
def promo(code):
    if code == promocode:
        return '{"valid":True}'
    else:
        return '{"valid":False}'


app.run("0.0.0.0",8000)