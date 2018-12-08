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
        if rend is self.RENDER:i
            if typ is self.FOL:
                return render_template('followship.html', users=data, rendTime=rendTime)
        return (data if rend else jsonify(data))
    
    def getsUserid(self, victim: str):
        _ = self.API.searchUsername(victim)
        return self.API.LastJson['user']['pk']
