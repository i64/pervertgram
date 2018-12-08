from typing import List, Dict, Tuple
from time import clock, sleep
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple

class libInsta:
    
    DELAY = 0
    
    def __init__(self, API: InstagramAPI):
        self.API = API

    def delay(self):
        self.DELAY += 1
        if self.DELAY % 50:
            sleep(1)
