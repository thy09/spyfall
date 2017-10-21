#! encoding=utf-8

# Creation Date: 2017-10-20 10:02:56
# Created By: Heyi Tang

from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask import g
import spyfall_game
import datetime
import os

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
    lower = int(request.args.get("lower", 1))
    locid = request.args.get("locid", "zh-cn-26")
    scene_count = int(request.args.get("scenecount", 10))
    spy_school = int(request.args.get("spyschool", 0))
    global spyfall
    if spyfall is None:
        spyfall = spyfall_game.SpyFalls()
    id = spyfall.create(count, upper, lower, scene_count, key = locid, spyschool = spy_school)
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
    cookie = request.cookies.get("ID%s" % (id))
    if cookie is not None:
        game["my_idx"] = cookie
    return jsonify(game)

@app.route("/roles")
def roles():
    locid = request.args.get("locid")
    scene = request.args.get("scene")
    data = spyfall.get_roles(locid, scene)
    return jsonify({"data":data})

@app.route("/set_cookie")
def set_cookie():
    g.language = ("zh-cn")
    id = request.args.get("id")
    cookie = request.args.get("cookie")
    if not cookie:
        return "FAIL"
    resp = app.make_response("OK")
    expire_time = datetime.datetime.now() + datetime.timedelta(seconds = 10)
    resp.set_cookie("ID%s" % id, value = cookie)
    return resp

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 24986)
