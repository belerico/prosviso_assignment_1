from flask import Flask, request, render_template, Markup
import requests
import logging

webapp = Flask(__name__)

@webapp.before_first_request
def setup_logging():
    logging.getLogger().setLevel(logging.INFO)

@webapp.route("/greetings", methods=["GET"])
def greetings():
        username = request.args.get("username")
        requests.post("http://api:7000/api/user/" + username)
        r = requests.get("http://api:7000/api/user/" + username).json()
        return render_template('index.html', 
                                delay=Markup("setTimeout(function(){ window.location.href = '/'; }, 10000);"),
                                text="Hello " + username + ", you\'ve visited this page " + r["count"] + " times. You will eventually be redirected in 10 seconds", 
                                delete_link=Markup('<a id="delete" href="http://0.0.0.0/delete?username=' + username + '">Delete me!</a>'))

@webapp.route("/delete", methods=["GET"])
def delete():
        username = request.args.get("username")
        r = requests.delete("http://api:7000/api/user/" + username)
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
        r = requests.delete("http://api:7000/api/users")
        if r.status_code == 200:
                r = r.json()
                return render_template('index.html',                      
                                        text=str(r["deleted"]) + " users has been deleted", 
                                        delete_link="")
        elif r.status_code == 404:
                return render_template('index.html',                              
                                        text="No user to delete", 
                                        delete_link="")
   
@webapp.route("/showall", methods=["GET"])
def showall():
        r = requests.get("http://api:7000/api/users/sort/desc").json()
        if r:
                table = ' \
                        <table class="table"> \
                                <thead> \
                                        <tr> \
                                        <th scope="col">#</th> \
                                        <th scope="col">User</th> \
                                        <th scope="col">Visits</th> \
                                        <th scope="col">Delete</th> \
                                        </tr> \
                                </thead> \
                '
                table_content = ''
                for i, couple in enumerate(r):
                        logging.info(couple)
                        table_content += ' \
                                <tr> \
                                        <th scope="row">' + str(i) + '</th> \
                                        <td>' + couple["username"] + '</td> \
                                        <td>' + couple["count"] + '</td> \
                                        <td><a href="http://0.0.0.0/delete?username=' + couple["username"] + '">Delete me!</a></td> \
                                </tr> \
                        '
                table += table_content + '</table>'
                return render_template('index.html',                                                                                             
                                        text=Markup(table), 
                                        delete_link="")
        else:
                return render_template('index.html',                
                                        text="No user to show", 
                                        delete_link="")
