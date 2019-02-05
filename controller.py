from time import clock, sleep
from flask import jsonify
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

    def getHdimage(self, victim: str):

        id = self.getsUserid(victim)
        _ = self.API.getUsernameInfo(id)
        data = self.API.LastJson['user']

        return jsonify([data])

    def getUsersFromID(self, pks, follow=None):
        users = list()
        if follow:
            for user in follow:
                if user['pk'] in pks:
                    users.append(user)
        else:
            for user in pks:
                _ = self.API.getUsernameInfo(user)
                users.append(self.API.LastJson)
        return users

    def getUserFollowings(self, victim: str,next_max_id=None):

        result = dict()
        user_id = self.getsUserid(victim)
        _ = self.API.getUserFollowings(user_id, maxid=next_max_id)
        self.delay()
        result['users'] = self.API.LastJson.get('users', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')
        
        return jsonify(result)

    def getUserFollowers(self, victim: str,next_max_id=None):

        result = dict()

        user_id = self.getsUserid(victim)
        next_max_id = True

        if next_max_id is True:
            next_max_id = ''
        _ = self.API.getUserFollowers(user_id, maxid=next_max_id)
        self.delay()

        result['users'] = self.API.LastJson.get('users', [])
        result['next'] = self.API.LastJson.get('next_max_id', '')
        
        return jsonify(result)

    def getMatches(self, victim: str):

        followers = self.getUserFollowers(
            victim)
        followings = self.getUserFollowings(
            victim)

        pks = set([i['pk'] for i in followers]) & set(
            [i['pk'] for i in followings])

        base = followers
        if len(followers) > len(followings):
            base = followings
        users = self.getUsersFromID(pks, base)

        return jsonify(users)

    def getLocationFeed(self, victim: int):

        images = list()
        next_max_id = True

        if next_max_id is True:
            next_max_id = ''
        _ = self.API.getLocationFeed(victim, maxid=next_max_id)
        self.delay()
        images.extend(self.API.LastJson.get('items', []))
        next_max_id = self.API.LastJson.get('next_max_id', '')

        return jsonify(next_max_id, images)

    def getLocationPeople(self, victim: int):

        images = self.getLocationFeed(victim)
        users = self.getUsersFromImages(images)
        tmp = list()
        _ = [tmp.append(i) for i in users if i not in tmp]

        return jsonify(tmp)

    def getUserImages(self, victim: str, last=0):

        items = list()
        id = self.getsUserid(victim)

        next_max_id = True
        counter = 0
        if last is not 0:
            counter += 1
            if counter >= last:
                return

        if next_max_id is True:
            next_max_id = ''
        _ = self.API.getUserFeed(id, maxid=next_max_id)
        items.extend(self.API.LastJson.get('items', []))
        next_max_id = self.API.LastJson.get('next_max_id', '')

        return jsonify(next_max_id, items)

    def getUserLocations(self, victim: str):
        locations = list()
        items = self.getUserImages(victim)
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
                
        return jsonify([victim, locations])
