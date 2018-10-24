from flask import Flask, request, render_template, jsonify, json
from redis import StrictRedis
from operator import itemgetter
import logging

webapp = Flask(__name__)
db = StrictRedis(host='redis', port=6379, db=0)

@webapp.before_first_request
def setup_logging():
    logging.getLogger().setLevel(logging.INFO)

@webapp.route("/greetings", methods=["POST"])
def greetings():
        db.incr(request.form.get("username"))
        name = request.form.get("username")
        count = db.get(request.form.get("username"))
        return render_template("index.html", deleted=False, name=name, count=count.decode('utf-8'))

@webapp.route("/api/all")
def get_all():
        data = []
        for key in db.scan_iter():
                data.append({'username': key.decode('utf-8'), 'count': db.get(key).decode('utf-8')})
        return jsonify(data)

@webapp.route("/api/delete/<username>")
def delete_user(username):
        db.delete(username)
        return render_template("index.html", deleted=True, name=username)


def sort_by_count(d):
    '''a helper function for sorting'''
    return d['count']

@webapp.route("/api/max")
def get_max():
        data = []
        for key in db.scan_iter():
                data.append({'username': key.decode('utf-8'), 'count': db.get(key).decode('utf-8')})
        logging.info(data)
        return sorted(data, key=sort_by_count)

@webapp.route("/api/<username>")
def get_count(username):
        if db.get(username) is None:
                return jsonify(username="Key not found"), 404
        else:
                return jsonify(username=username, count=db.get(username).decode('utf-8')), 200

@webapp.route("/prova")
def prova():
        return "Prova"
   
