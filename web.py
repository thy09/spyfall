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

@app.before_request
def before_request():
    global spyfall
    if spyfall is None:
        spyfall = spyfall_game.SpyFalls()
    uid = request.cookies.get("UID")
    if not uid or not spyfall.exist_user(uid):
        uid = spyfall.new_user()
    spyfall.update_user(uid)
    g.uid = uid

@app.after_request
def after_request(resp):
    uid = request.cookies.get("UID")
    if uid != g.uid:
        resp.set_cookie("UID", g.uid)
    return resp

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
    data = {"game":game}
    for idx, uid in enumerate(game["occupied"]):
        if uid == g.uid:
            data["my_idx"] = idx
        if not spyfall.exist_user(uid):
            game["occupied"][idx] = None
    return jsonify(data)

@app.route("/roles")
def roles():
    locid = request.args.get("locid")
    scene = request.args.get("scene")
    data = spyfall.get_roles(locid, scene)
    return jsonify({"data":data})

@app.route("/sit")
def sit():
    id = request.args.get("id")
    idx = request.args.get("idx")
    if spyfall.user_sit(id, idx, g.uid):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"OCCUPIED"})

@app.route("/show_users")
def show_users():
    result = {}
    for k,v in spyfall.users.items():
        result[k] = str(v)
    return jsonify(result)
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 24986)
