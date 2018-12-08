from typing import List, Dict, Tuple
from time import clock, sleep
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import jsonify
from typing import List, Dict, Tuple

class libInsta:
    def __init__(self, API: InstagramAPI):
        self.API = API
