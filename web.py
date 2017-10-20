#! encoding=utf-8

# Creation Date: 2017-10-20 10:02:56
# Created By: Heyi Tang

from flask import Flask, render_template, redirect, request, url_for, jsonify
import spyfall_game

app = Flask(__name__)
app.config["SECRET_KEY"] = 'spyfallneverguess'

spyfall = None

@app.route("/")
def index():
    return redirect(url_for(".create", count = 8))

@app.route("/create")
def create():
    count = int(request.args.get("count", 8))
    if count<3:
        return "INVALID_PLAYER_COUNT"
    upper = int(request.args.get("upper", (count+7)/8))
    lower = int(request.args.get("lower", 0))
    global spyfall
    if spyfall is None:
        spyfall = spyfall_game.SpyFall("words.json")
    id = spyfall.create(count, upper, lower)
    return redirect(url_for(".play", id = id))

@app.route("/play")
def play():
    id = request.args.get("id", 0)
    global spyfall
    if spyfall is None or spyfall.game(id) is None:
        return redirect(url_for(".create", count = 8))
    game = spyfall.game(id)
    return render_template("game.html", game = game)

@app.route("/status")
def status():
    id = request.args.get("id", 0)
    game = spyfall.game(id)
    return jsonify(game)

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 24987)
