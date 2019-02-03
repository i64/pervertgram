from flask import Flask, request, render_template
from json import dumps
import json
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple
from time import clock
from controller import libInsta
from flask_restful import Resource, Api

CONFIG_PATH = 'config.json'
creds = json.load(open(CONFIG_PATH))


levAPI = InstagramAPI(creds['username'], creds['pwd'])
levAPI.login()

app = Flask(__name__)
api = Api(app)

insta = libInsta(levAPI)


class getUserFollowings(Resource):
    def get(self, victim):
        return insta.getUserFollowings(victim)


class getUserFollowers(Resource):
    def get(self, victim):
        return insta.getUserFollowers(victim)


class getMatches(Resource):
    def get(self, victim):
        return insta.getMatches(victim)


class getLocationPeople(Resource):
    def get(self, victim):
        return insta.getLocationPeople(victim)


class getLocationFeed(Resource):
    def get(self, victim):
        return insta.getLocationFeed(victim)


class getHdimage(Resource):
    def get(self, victim):
        return insta.getHdimage(victim)


api.add_resource(getUserFollowings, '/followings/<victim>')
api.add_resource(getUserFollowers, '/folllowers/<victim>')
api.add_resource(getMatches, '/match/<victim>')
api.add_resource(getLocationPeople, '/location-people/<victim>')
api.add_resource(getLocationFeed, '/location/<victim>')
api.add_resource(getHdimage, '/dp/<victim>')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port='5002', debug=True)
