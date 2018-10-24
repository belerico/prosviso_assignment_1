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
        
@webapp.route("/prova")
def prova():
        return "Prova"
   
