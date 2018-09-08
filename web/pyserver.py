import redis
import falcon
from web3 import Web3, HTTPProvider
from falcon_cors import CORS

PREFIX = "CANDIDATES"
r = redis.StrictRedis(host='localhost', port=6379, db=0)
cors = CORS(allow_all_origins=True)
app = falcon.API(middleware=[cors.middleware])


def convert(data):
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, (str, int)):
        return str(data)
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return tuple(map(convert, data))
    if isinstance(data, list):
        return list(map(convert, data))
    if isinstance(data, set):
        return set(map(convert, data))
    return data


def get(route):
    def get_decorator(func):
        class Getter(object):
            def on_get(self, req, resp):
                """Handles GET Requests"""
                resp.media = convert(func(req, resp))

        app.add_route(route, Getter())
    return get_decorator


def post(route):
    def post_decorator(func):
        class Poster(object):
            def on_post(self, req, resp):
                """Handles POST Requests"""
                func(req.media, resp)

        app.add_route(route, Poster())
    return post_decorator


@get("/getCandidates")
def get_candidates(_req, _resp):
    return r.hgetall(PREFIX)


@post("/addCandidates")
def post_candidates(req, _resp):
    if "candidate" not in req or "address" not in req:
        return
    r.hset(PREFIX, req["address"], req["candidate"])


# web3 connection


# web3x = Web3(HTTPProvider('http://localhost:7545'))
# filter_hash = web3x.sha3("NEWVOTE").hex()
# vote_filter = web3x.eth.filter({"eventType": filter_hash})
