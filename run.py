import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash


app = Flask(__name__)


def write_to_file(filename, data):
    """handle the process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)


def add_answer(username, answer):
    """Add messages to the 'messages' list"""
    write_to_file("data/answers.txt", "{0}\n{2}\n".format(
            username.title(),
            answer
            ))


def get_all_answers():
    """Get all of the messages and separate them by a 'br'"""
    answers = []
    with open("data/answers.txt", "r") as riddle_answers:
        answers = riddle_answers.readlines()
    return answers


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        with open("data/online_users.txt", "r+") as file:
            for line in file: # 2: If name already exists in file, skip this and redirect to username page
                if request.form["username"].lower() in line:
                    return redirect(request.form['username'].lower())
            else: # 1: if name is not in file, add it then redirect to username page
                file.write(request.form["username"].lower() + "\n")
        return redirect(request.form['username']) # 3: redirect to username page
    return render_template("index.html", page_title="Home")


@app.route('/about')
def about():
    return render_template("about.html", page_title="About")


@app.route('/highscores')
def highscores():
    data = []
    with open('data/highscores.json', 'r') as json_data:
        data = json.load(json_data)
        
    return render_template("highscores.html", page_title="Highscores", highscores=data)


@app.route("/<username>", methods=["GET", "POST"])
def user(username):
    
    with open("data/riddles.json", "r") as json_data:
        data = json.load(json_data)
            
    if request.method == "POST" and username == username:

        return render_template("game.html",
                                page_title="Game",
                                riddles=data)
                                
    return render_template("welcome.html",
                            username=username)


# @app.route('/about/<member_name>')
# def about_member(member_name):
#     member = {}
    
#     with open('data/company.json', 'r') as json_data:
#         data = json.load(json_data)
#         for obj in data:
#             if obj["url"] == member_name:
#                 member = obj
    
#     return render_template("member.html", member=member)


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == "POST":
#         flash("Thanks {}, we have recieved your message!".format(request.form["name"]))
#     return render_template("contact.html", page_title="Contact")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)