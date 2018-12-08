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
    IMAGE = 1

    JSON = 0
    RENDER = 1
    RAW = 2
    
    API = 0
    ALL = 1
    NAN = 0

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
            elif typ is self.IMAGE:
                return render_template('imageship.html', images=data, rendTime=rendTime)
 
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

    def getMatch(self, victim: str, rend: int):
        tic = clock()

        followers = self.getUserFollowers(victim, self.RAW, self.ALL)
        followings = self.getUserFollowings(victim, self.RAW, self.ALL)

        pks = set([i['pk'] for i in followers]) & set(
            [i['pk'] for i in followings])

        base = followers
        if len(followers) > len(followings):
            base = followings
        users = self.getUsersFromID(pks, base)

          toc = clock()
        rendTime = toc - tic
        return self.imgfy(users, rendTime, rend)
    
    def getLocationFeed(self, victim: int, rend: int, getAll=0):
        tic = clock()
        images = list()
        if getAll:
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getLocationFeed(victim, maxid=next_max_id)
                self.delay()
                images.extend(self.API.LastJson.get('items', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
        else:
            _ = self.API.getLocationFeed(victim)
            images.extend(self.API.LastJson.get('ranked_items', []))
        toc = clock()
        rendTime = toc - tic
        return self.imgfy(images, rendTime, rend, typ=getAll)

    def getLocationPeople(self, victim: int, rend: int, getAll=0):
        tic = clock()
        images = self.getLocationFeed(victim, self.RAW, getAll)
        users = self.getUsersFromImages(images)
        tmp = list()
        _ = [tmp.append(i) for i in users if i not in tmp]
        users = tmp
        del(tmp)
        toc = clock()
        rendTime = toc - tic
        return self.imgfy(users, rendTime, rend)

    def getUserImages(self, victim: str, rend: int, all=None, last=0):
        tic = clock()
        items = list()
        id = self.getsUserid(victim)

        if all:
            next_max_id = all
            counter = 0
            while next_max_id:

                if last is not 0:
                    counter += 1
                    if counter >= last:
                        break

                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFeed(id, maxid=next_max_id)
                items.extend(self.API.LastJson.get('items', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
        else:
            _ = self.API.getUserFeed(id)
            items = self.API.LastJson['items']

        rendTime = clock() - tic
        return self.imgfy(items, rendTime, rend, self.IMAGE)
