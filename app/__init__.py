from flask import Flask
from mongoengine import *

from app.model import *


connect("mininote_test")


mininote = Flask(__name__)

import app.api