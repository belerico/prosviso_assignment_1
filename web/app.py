from flask import Flask, request, render_template
from redis import StrictRedis

application = Flask(__name__)
db = StrictRedis(host='redis', port=6379, db=0)


@application.route("/greetings", methods=["POST"])
def greetings():
        db.incr(request.form.get("username"))
        name = request.form.get("username")
        count = db.get(request.form.get("username"))
        return render_template("index.html", name=name, count=int(count))

@application.route("/prova")
def prova():
        return "Prova"
   
