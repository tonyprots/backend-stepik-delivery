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

"""
{"address": "Nagatinskaya, 7a", "status": "CANCELLED", "meals": [1, 2], "id": "becc6c68-835c-4e84-b1ef-f92962a1d7c1", "summ": 288.0, "ordered": 1559574456.457047}, 
{"address": "Nagatinskaya, 7a", "status": "CANCELLED", "meals": [1, 2], "id": "dc4ba93a-1b65-4e78-8d48-928e7b473524", "summ": 201.6, "ordered": 1559574496.381071}]
"""


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0, 2)
    promotions = file_read('promotions.json')
    return json.dumps(promotions[promotion_number], ensure_ascii=False)


