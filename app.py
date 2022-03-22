import io
import json
from types import SimpleNamespace

import secrets
from datetime import datetime

from flask import Flask
from werkzeug.exceptions import HTTPException

def json2obj(s):
  if isinstance(s, io.IOBase):
    s = s.read()
  obj = json.loads(s, object_hook=lambda d: SimpleNamespace(**d))
  return obj

def obj2dict(obj):
  d = json.loads(json.dumps(obj, default=lambda s: vars(s)))
  return d

tracingId = secrets.token_hex(20)

app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/")
def hello_world():
  return "Hello, World!\n"

@app.route("/yapily/institutions")
def yapily_institutions():
  f = open('yapily/institutions.json')
  d = json2obj(f)
  d.meta.tracingId = tracingId 
  data = obj2dict(d)
  return data
