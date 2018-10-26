from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from redis import StrictRedis
import logging

flaskAPI = Flask(__name__)
api = Api(flaskAPI)
db = StrictRedis(host='redis', port=6379, db=0)

def get_all_user():
        data = []
        for key in db.scan_iter():
                data.append({'count':db.get(key).decode('utf-8'),'username':key.decode('utf-8')})
        return data

def sort_json(data, type, key_func):
        if (type == "desc"):
                return sorted(data, key=key_func, reverse=True)
        else:
                return sorted(data, key=key_func)

@flaskAPI.before_first_request
def __setup_logging():
    logging.getLogger().setLevel(logging.INFO)

class UserActions(Resource):
        def get(self, username):
                count = db.get(username)
                if count is None:
                        abort(404)
                else:
                        return jsonify({'count':count.decode('utf-8'),'username':username})
        
        def delete(self, username):
                deleted = db.delete(username)
                if deleted == 0:
                        abort(404)
                else:
                        return '', 200  
        
        def post(self, username):
                return jsonify(db.incr(username))

class AllUsersActions(Resource):
        def get(self):
                data = get_all_user()
                return jsonify(data)
      
        def delete(self):
                if db.dbsize() == 0:
                        abort(404)
                else: 
                        for key in db.scan_iter():
                                db.delete(key)
                        return '', 200

class GetAllUsersSorted(Resource):
        def get(self, type):
                data = sort_json(get_all_user(), type, lambda x: (int(x['count']), x['username']))
                return jsonify(data)

class Func(Resource):
        def get(self, type):
                data = get_all_user()
                if (type == "max"):
                        max_tuple = max(data, key=lambda x: int(x['count']))
                        max_tuples = [{"count":i["count"],"username":i["username"]} for i in data if i["count"]==max_tuple["count"]]
                        return jsonify(max_tuples)
                elif (type == "min"):
                        min_tuple = min(data, key=lambda x: int(x['count']))
                        min_tuples = [{"count":i["count"],"username":i["username"]} for i in data if i["count"]==min_tuple["count"]]
                        return jsonify(min_tuples)

api.add_resource(UserActions, '/api/<username>')
api.add_resource(AllUsersActions, '/api/all')
api.add_resource(Func, '/api/func/<type>')
api.add_resource(GetAllUsersSorted, '/api/func/sort/<type>')
