from flask import Flask, request, render_template
from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import jsonify
import json

from controller import libInsta

CONFIG_PATH = 'config.json'
creds = json.load(open(CONFIG_PATH))


levAPI = InstagramAPI(creds['username'], creds['pwd'])
levAPI.login()

app = Flask(__name__)
api = Api(app)

instalib = libInsta(levAPI)


class getUserFollowings(Resource):
    def get(self, victim, next=None):
        return instalib.getUserFollowings(victim, next_max_id=next)


class getUserFollowers(Resource):
    def get(self, victim, next=None):
        return instalib.getUserFollowers(victim, next_max_id=next)


class getMatches(Resource):
    def get(self, victim):
        return instalib.getMatches(victim)


class getLocationPeople(Resource):
    def get(self, victim):
        return instalib.getLocationPeople(victim)


class getLocationFeed(Resource):
    def get(self, victim):
        return instalib.getLocationFeed(victim)


class getHdimage(Resource):
    def get(self, victim):
        return instalib.getHdimage(victim)


api.add_resource(getUserFollowings, '/api/followings/<victim>/',
                 '/api/followings/<victim>/<next>')
api.add_resource(getUserFollowers,  '/api/followers/<victim>/',
                 '/api/followers/<victim>/<next>')

api.add_resource(getMatches,        '/api/match/<victim>')
api.add_resource(getLocationPeople, '/api/location-people/<victim>')
api.add_resource(getLocationFeed,   '/api/location/<victim>')
api.add_resource(getHdimage,        '/api/dp/<victim>')


@app.route('/followings/<victim>')
def viewFollowings(victim):
    return render_template('followship.html')


@app.route('/followers/<victim>')
def viewFollowers(victim):
    return render_template('followship.html')


@app.route('/match/<victim>')
def viewMatches(victim):
    return render_template('followship.html')


@app.route('/location-people/<int:location>')
def viepHeatmap(data):
    return render_template('heatmap.html')


@app.route('/location/<int:location>')
def viewLocation(victim):
    return render_template('imageship.html')


@app.route('/dp/<victim>')
def viewDP(victim):
    return render_template('imageship.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port='5002', debug=True)
