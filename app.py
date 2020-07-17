from flask import Flask, render_template, jsonify
from interface import Pervertgram

with open("config.json") as config:
    CREDENTIALS = __import__("json").load(config)

interface = Pervertgram(CREDENTIALS.get("username"), CREDENTIALS.get("password"))
app = Flask(__name__)


@app.route("/api/followings/<username>/", defaults={"next_max_id": None})
@app.route("/api/followings/<username>/<next_max_id>")
def api_user_followings(username: str, next_max_id: str):
    return jsonify(interface.followings(username, next_max_id=next_max_id))


@app.route("/api/followers/<username>/", defaults={"next_max_id": None})
@app.route("/api/followers/<username>/<next_max_id>")
def api_user_followers(username: str, next_max_id: str):
    return jsonify(interface.followers(username, next_max_id=next_max_id))


@app.route("/api/match/<username>/")
def api_matches(username: str):
    return jsonify(interface.followed_back(username))


@app.route("/api/location/<username>/", defaults={"next_max_id": None})
@app.route("/api/location/<username>/<next_max_id>")
def api_location_feed(username: str, next_max_id: str):
    return jsonify(interface.location_ppl(username, next_max_id=next_max_id))


@app.route("/api/dp/<username>")
def api_hdimage(username: str):
    return jsonify(interface.hd_pfp(username))


@app.route("/api/location-people/<int:location>")
def api_location_people(location: int):
    return jsonify(interface.location_ppl(location))


@app.route("/api/profile_locations/<username>")
def api_profile_locations(username):
    return jsonify(interface.profile_locations(username))


@app.route("/api/likers/<picture_code>")
def api_profile_liker(picture_code: str):
    return jsonify(interface.liker(picture_code))


@app.route("/followings/<username>")
def followings(username: str):
    return render_template("followship.html", with_page=True)


@app.route("/followers/<username>")
def followers(username: str):
    return render_template("followship.html", with_page=True)


@app.route("/match/<username>")
def matches(username: str):
    return render_template("followship.html")


@app.route("/location-people/<int:location>")
def location_people(location: int):
    return render_template("followship.html")


@app.route("/heatmap/<username>")
def heatmap(username: str):
    return render_template("heatmap.html")


@app.route("/dp/<username>")
def pfp(username: str):
    return render_template("dp.html", image_url=interface.hd_pfp(username))


@app.route("/likers/<picture_code>")
def liker(picture_code: str):
    return render_template("followship.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5002", debug=True)
