import os, requests
from flask import Flask, request, render_template, jsonify

import get_food_data
from datetime import date



app = Flask(__name__, static_folder="public", template_folder="views")

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get("SECRET")


@app.route("/")
def tageskarte():
    today = date.today()
    restaurant_liste = []
    for i in range(1, 4):
        r = get_food_data.Restaurants(str(i))
        tageskarte, button_link = r.get_tageskarte() # tageskarte = ["text", "datum"]
        tageskarte_inhalt = {
            "name": r.FULL_NAME,
            "address": r.ADDRESS,
            "tageskarte": tageskarte[0],
            "created_at" : tageskarte[1],
            "button_link": button_link
        }
        restaurant_liste.append(tageskarte_inhalt)

    return render_template("index.html", restaurants=restaurant_liste, today=today)


if __name__ == "__main__":
    app.run(debug=True)
