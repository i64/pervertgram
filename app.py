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
    def get(self, victim, next=''):
        return jsonify(instalib.getUserFollowings(victim, next_max_id=next))


class getUserFollowers(Resource):
    def get(self, victim, next=''):
        return jsonify(instalib.getUserFollowers(victim, next_max_id=next))


class getMatches(Resource):
    def get(self, victim):
        return jsonify(instalib.getMatches(victim))


class getLocationPeople(Resource):
    def get(self, victim, next=''):
        return jsonify(instalib.getLocationPeople(victim))


class getLocationFeed(Resource):
    def get(self, victim, next=''):
        return jsonify(instalib.getLocationFeed(victim, next_max_id=next))


class getHdimage(Resource):
    def get(self, victim):
        return jsonify(instalib.getUserInfo(victim))


class getUserLocations(Resource):
    def get(self, victim):
        return jsonify(instalib.getUserLocations(victim))


api.add_resource(getUserFollowings, '/api/followings/<victim>/',
                 '/api/followings/<victim>/<next>')
api.add_resource(getUserFollowers,  '/api/followers/<victim>/',
                 '/api/followers/<victim>/<next>')

api.add_resource(getMatches,        '/api/match/<victim>/')
api.add_resource(getLocationPeople, '/api/location-people/<victim>/',
                 '/api/location-people/<victim>/<next>')
api.add_resource(getLocationFeed,   '/api/location/<victim>/',
                 '/api/location/<victim>/<next>')

api.add_resource(getHdimage,        '/api/dp/<victim>')

api.add_resource(getUserLocations,        '/api/user-locations/<victim>')

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
def viewLocationPeople(location):
    return render_template('people.html')


@app.route('/heatmap/<victim>')
def viewHeatmap(victim):
    return render_template('heatmap.html')


@app.route('/location/<int:location>')
def viewLocation(location):
    return render_template('imageship.html')


@app.route('/dp/<victim>')
def viewDP(victim):
    return render_template('dp.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port='5002', debug=True)
