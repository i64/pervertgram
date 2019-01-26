from typing import List, Dict, Tuple
from time import clock, sleep
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from json import dumps
import json
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple
import cons

class libInsta:

    delayTime = 0

    def __init__(self, API: InstagramAPI):
        self.API = API

    def delay(self):
        self.delayTime += 1
        if self.delayTime % 100:
            sleep(1)

    def getsUserid(self, victim: str):
        _ = self.API.searchUsername(victim)
        return self.API.LastJson['user']['pk']

    def getUsersFromImages(self, images: List[dict]):
        return [image['user'] for image in images]

    def getHdimage(self, victim: str, rend):
        tic = clock()
        id = self.getsUserid(victim)
        _ = self.API.getUsernameInfo(id)
        data = self.API.LastJson['user']
        toc = clock()
        rendTime = tic - toc
        return self.imgfy([data], rendTime, rend, typ=cons.Template.IMAGE)

    def imgfy(self, data, rendTime: float, rend: int, typ=0):
        if rend is cons.Render.RENDER:
            if typ is cons.Template.FOL:
                return render_template('followship.html', users=data, rendTime=rendTime)

            elif typ is cons.Template.IMAGE:
                return render_template('imageship.html', images=data, rendTime=rendTime)

            elif typ is cons.Template.MAP:
                return render_template('heatmap.html', username=data[0])

        if typ is cons.Template.MAP:
            data = data.pop()
        return (data if rend else jsonify(data))

    def getUsersFromID(self, pks: List[int], follow=None):
        users = list()
        if follow:
            for i in follow:
                if i['pk'] in pks:
                    users.append(i)
        else:
            for i in pks:
                _ = self.API.getUsernameInfo(i)
                users.append(self.API.LastJson)
        return users

    def getUserFollowings(self, victim: str, rend: int, getAll: int):
        tic = clock()
        users = list()
        user_id = self.getsUserid(victim)
        if getAll:
            next_max_id = True
            while next_max_id:
                if next_max_id is True:
                    next_max_id = ''
                _ = self.API.getUserFollowings(user_id, maxid=next_max_id)
                self.delay()
                users.extend(self.API.LastJson.get('users', []))
                next_max_id = self.API.LastJson.get('next_max_id', '')
        else:
            _ = self.API.getUserFollowings(user_id)
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

    def match(self, victim: str, rend: int):
        tic = clock()

        followers = self.getUserFollowers(victim, cons.Render.RAW, cons.Ret.ALL)
        followings = self.getUserFollowings(victim, cons.Render.RAW, cons.Ret.ALL)

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
        images = self.getLocationFeed(victim, cons.Render.RAW, getAll)
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
        return self.imgfy(items, rendTime, rend, cons.Template.IMAGE)

    def getUserLocations(self, victim: str, rend: int, last=0):
        locations = list()
        items = self.getUserImages(victim, cons.Render.RAW, cons.Ret.ALL, last)
        for item in items:
            if item.get('location', None) is None:
                pass
            else:
                data = dict()
                # data['id']
                if item.get("image_versions2", None):
                    data['source'] = item['image_versions2']['candidates'][0]['url']
                else:
                    data['source'] = item['carousel_media'][0]['image_versions2']['candidates'][0]['url']
                data['link'] = item['code']
                data['location'] =(item['location']['short_name'] if item['location'].get('short_name',None) else item['location']['name'])
                data['latitude'] = item['location']['lat']
                data['longitude'] = item['location']['lng']
                locations.append(data)
        return self.imgfy([victim, locations], 0, rend, cons.Template.MAP)
