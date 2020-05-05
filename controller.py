from time import clock, sleep
from flask import jsonify, json
from InstagramAPI import InstagramAPI

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

    def getUsersFromImages(self, images):
        return [image['user'] for image in images]

    def getUserInfo(self, victim: str):
        id = self.getsUserid(victim)
        _ = self.API.getUsernameInfo(id)

        return self.API.LastJson['user']

    def getUsersFromID(self, pks, follow=None):
        users = list()
        if follow:
            for user in follow:
                if user['pk'] in pks:
                    users.append(user)
        else:
            for pk in pks:
                _ = self.API.getUsernameInfo(pk)
                users.append(self.API.LastJson['user'])
        return users

    def getUserFollowings(self, victim: str, next_max_id=None):
        result = dict()
        user_id = self.getsUserid(victim)
        _ = self.API.getUserFollowings(user_id, maxid=next_max_id)
        self.delay()
        result['users'] = self.API.LastJson.get('users', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')

        return result

    def getUserFollowers(self, victim: str, next_max_id=''):
        result = dict()
        user_id = self.getsUserid(victim)
        _ = self.API.getUserFollowers(user_id, maxid=next_max_id)
        self.delay()
        result['users'] = self.API.LastJson.get('users', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')

        return result

    def getMatches(self, victim: str):
        followers = list()
        followings = list()

        next = True
        while(next):
            _ = self.getUserFollowers(
                victim, ('' if next == True else next))
            next = _['next']
            followers.extend(_['users'])
        next = True
        while(next):
            _ = self.getUserFollowings(
                victim, ('' if next == True else next))
            next = _['next']
            followings.extend(_['users'])   

        pks = set([follower['pk'] for follower in followers]) & set(
            [following['pk'] for following in followings])

        base = followers
        if len(followers) > len(followings):
            base = followings
        users = self.getUsersFromID(pks, base)

        return users

    def getLocationFeed(self, victim: int, next_max_id=''):
        result = dict()
        _ = self.API.getLocationFeed(victim, maxid=next_max_id)
        self.delay()
        result['items'] = self.API.LastJson.get('items', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')

        return result

    def getLocationPeople(self, victim: int):
        images = list()
        next = True
        while(next):
            _ = self.getLocationFeed(
                victim, ('' if next == True else next))
            next = _['next']
            images.extend(_['items'])
        users = list()
        _ = [users.append(user) for user in self.getUsersFromImages(
            images) if user not in users]

        return users

    def getUserImages(self, victim: str, next=''):
        result = dict()
        _ = self.API.getUserFeed(self.getsUserid(victim), maxid=next)
        result['items'] = self.API.LastJson.get('items', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')

        return result

    def getUserLocations(self, victim: str):
        locations = list()
        items = list()

        next = True
        while(next):
            _ = self.getUserImages(
                victim, ('' if next == True else next))
            next = _['next']

            items.extend(_['items'])

        for item in items:
            if item.get('location', None) is None:
                pass
            else:
                data = dict()
                if item.get("image_versions2", None):
                    data['source'] = item['image_versions2']['candidates'][0]['url']
                else:
                    data['source'] = item['carousel_media'][0]['image_versions2']['candidates'][0]['url']
                data['link'] = item['code']
                data['location'] = (item['location']['short_name'] if item['location'].get(
                    'short_name', None) else item['location']['name'])
                data['latitude'] = item['location']['lat']
                data['longitude'] = item['location']['lng']
                locations.append(data)
        return locations
