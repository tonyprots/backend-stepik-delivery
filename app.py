from flask import Flask
app = Flask(__name__)

promotion_text = 0


@app.route("/")
def hello():
    return "<h1>" +"Test" +"</h1"


@app.route("/alive")
def alive():
    return'{"alive":true}'

@app.route("/workhours")
def workours():
    return '{"opens":"10:00", "closes":"20:00"}'

#@app.route("/promotion")
#def

app.run("0.0.0.0",8000)