from flask import Flask, request, render_template, Markup
from redis import StrictRedis
import requests
import logging

webapp = Flask(__name__)

@webapp.before_first_request
def setup_logging():
    logging.getLogger().setLevel(logging.INFO)

@webapp.route("/greetings", methods=["GET"])
def greetings():
        username = request.args.get("username")
        requests.post("http://api:7000/api/" + username)
        r = requests.get("http://api:7000/api/" + username).json()
        return render_template('index.html', 
                                text="Hello " + username + ", you\'ve visited this page " + r["count"] + " times", 
                                delete_link=Markup('<a id="delete" href="http://0.0.0.0/delete?username=' + username + '">Delete me!</a>'))

@webapp.route("/delete", methods=["GET"])
def delete():
        username = request.args.get("username")
        r = requests.delete("http://api:7000/api/" + username)
        if r.status_code == 200:
                return render_template('index.html', 
                                        text="User " + username + " has been deleted", 
                                        delete_link="")
        elif r.status_code == 404:
                return render_template('index.html', 
                                        text="User " + username + " doesn\'t exist anymore", 
                                        delete_link="")

@webapp.route("/deleteall", methods=["GET"])
def deleteall():
        r = requests.delete("http://api:7000/api/all")
        if r.status_code == 200:
                return render_template('index.html', 
                                        text="All users has been deleted", 
                                        delete_link="")
        elif r.status_code == 404:
                return render_template('index.html', 
                                        text="No user to delete", 
                                        delete_link="")
   
