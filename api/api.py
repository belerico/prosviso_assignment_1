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

@flaskAPI.before_first_request
def __setup_logging():
    logging.getLogger().setLevel(logging.INFO)

class User(Resource):
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

class AllUser(Resource):
        def get(self):
                data = get_all_user()
                return jsonify(data)
      
        def delete(self):
                size = db.dbsize()
                if size == 0:
                        abort(404)
                else: 
                        for key in db.scan_iter():
                                db.delete(key)
                        return jsonify({"deleted":size})

class Sort(Resource):
        def get(self, type):
                if type == "desc":
                        data = sorted(get_all_user(), key=lambda x: (-int(x['count']), x['username']))
                elif type == "asc":
                        data = sorted(get_all_user(), key=lambda x: (int(x['count']), x['username']))
                else:
                        abort(404)
                return jsonify(data)

class Func(Resource):
        def get(self, function):
                data = get_all_user()
                if data:
                        if function == "max":
                                max_tuple = max(data, key=lambda x: int(x['count']))
                                max_tuples = [{"count":i["count"],"username":i["username"]} for i in data if i["count"]==max_tuple["count"]]
                                return jsonify(max_tuples)
                        elif function == "min":
                                min_tuple = min(data, key=lambda x: int(x['count']))
                                min_tuples = [{"count":i["count"],"username":i["username"]} for i in data if i["count"]==min_tuple["count"]]
                                return jsonify(min_tuples)
                        else: 
                                abort(404)
                else:       
                        return jsonify([])

class Count(Resource):
        def get(self):
                return jsonify({"count":db.dbsize()})

api.add_resource(User, '/api/user/<username>')
api.add_resource(AllUser, '/api/users')
api.add_resource(Func, '/api/users/<function>')
api.add_resource(Count, '/api/users/count')
api.add_resource(Sort, '/api/users/sort/<type>')
