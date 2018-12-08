from flask import Flask, request, render_template
from flask_restful import Resource, Api
from json import dumps
import json
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple
from time import clock
from libInsta import libInsta

CONFIG_PATH = 'config.json'
creds = json.load(open(CONFIG_PATH))


API = InstagramAPI(creds['username'], creds['pwd'])
API.login()

app = Flask(__name__)

insta = libInsta(API)

@app.route('/followings/<victim>')
@app.route('/followings/<victim>/<int:rend>')
@app.route('/followings/<victim>/<int:rend>/<int:getAll>')
def getUserFollowings(victim, rend=1, getAll=0):
    return insta.getUserFollowings(victim, rend, getAll=getAll)


@app.route('/followers/<victim>')
@app.route('/followers/<victim>/<int:rend>')
@app.route('/followers/<victim>/<int:rend>/<int:getAll>')
def getUserFollowers(victim, rend=1, getAll=0):
    return insta.getUserFollowers(victim, rend, getAll=getAll)


@app.route('/match/<victim>')
@app.route('/match/<victim>/<int:rend>')
def match(victim, rend=1):
    return insta.match(victim, rend)


@app.route('/location-people/<int:location>')
@app.route('/location-people/<int:location>/<int:rend>')
@app.route('/location-people/<int:location>/<int:rend>/<int:getAll>')
def getLocationPeople(location: int, rend=1, getAll=0):
    return insta.getLocationPeople(location, rend, getAll)


@app.route('/location/<int:location>')
@app.route('/location/<int:location>/<int:rend>')
@app.route('/location/<int:location>/<int:rend>/<int:getAll>')
def getLocationFeed(location: int, rend=1, getAll=1):
    return insta.getLocationFeed(location, rend, getAll)


@app.route('/dp/<victim>')
@app.route('/dp/<victim>/<int:rend>')
def getHdimage(victim: int, rend=1):
    return insta.getHdimage(victim, rend)
# api.add_resource(getUserFollowings, '/followings/<victim>/<int:render>')
@app.route('/heatmap/<victim>')
@app.route('/heatmap/<victim>/<int:rend>')
def getHeatmap(victim,rend=1):
    return insta.getUserLocations(victim,rend)

# api.add_resource(getUserFollowers, '/followers/<victim>')  # Route_3
if __name__ == '__main__':
    app.run(host="127.0.0.1",port='5002', debug=True)

