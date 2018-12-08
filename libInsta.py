from typing import List, Dict, Tuple
from time import clock, sleep
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple

class libInsta:
    
    DELAY = 0
    FOL = 0

    JSON = 0
    RENDER = 1
    RAW = 2

    def __init__(self, API: InstagramAPI):
        self.API = API

    def delay(self):
        self.DELAY += 1
        if self.DELAY % 50:
            sleep(1)

    def imgfy(self, data, rendTime: float, rend: int, typ=0):
        if rend is self.RENDER:
            if typ is self.FOL:
                return render_template('followship.html', users=data, rendTime=rendTime)
        return (data if rend else jsonify(data))
    
    def getsUserid(self, victim: str):
        _ = self.API.searchUsername(victim)
        return self.API.LastJson['user']['pk']

    def getUserFollowers(self, victim: str, rend: int, getAll: int):
        tic = clock()
        users = list()
        user_id = self.getsUserid(victim)
        if getAll:
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFollowers(user_id, maxid=next_max_id)
                self.delay()
                users.extend(self.API.LastJson.get('users', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
        else:
            _ = self.API.getUserFollowers(user_id)
            users = self.API.LastJson['users']

        toc = clock()
        rendTime = toc - tic
        return self.imgfy(users, rendTime, rend)

    def getUserFollowers(self, victim: str, rend: int, getAll: int):
        tic = clock()
        users = list()
        user_id = self.getsUserid(victim)
        if getAll:
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFollowers(user_id, maxid=next_max_id)
                self.delay()
                users.extend(self.API.LastJson.get('users', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
        else:
            _ = self.API.getUserFollowers(user_id)
            users = self.API.LastJson['users']

        toc = clock()
        rendTime = toc - tic
        return self.imgfy(users, rendTime, rend)
