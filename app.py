#!/usr/bin/env python

import flask
from flask import request, redirect, url_for, send_from_directory, session

import random as rand
import os

from modes import modes

import json

# Create the application.
APP = flask.Flask(__name__)
APP.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@APP.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@APP.route('/question')
def question():
    num, max_num, game_mode = session["num"], session["max_num"], session["game_mode"]
    targetList=modes[game_mode]
    possibilities=rand.sample(targetList, 5 if 5<len(targetList) else len(targetList))
    sp=rand.choice(possibilities)
    with open('Data/fish.json', 'r') as file:
        images = json.load(file)
    if len(images[sp])!=0:
        url=rand.choice(images[sp])
    if int(num)<=int(max_num):
        return flask.render_template('question.html', 
                                    num=num, max_num = max_num, 
                                    game_mode=game_mode, possibilites=possibilities, 
                                    correct=sp,  url=url)
    else:
        return redirect(url_for("menu"))

@APP.route('/results')
def results():
    correct, max_num, game_mode = session["correct"], session["max_num"], session["game_mode"]
    return flask.render_template('results.html', 
                                correct=correct, max_num = max_num, 
                                game_mode=game_mode)

@APP.route('/response/<response>/<correct>')
def response(response, correct):
    num, max_num, game_mode = session["num"], session["max_num"], session["game_mode"]
    session["num"]+=1
    if response==correct: session["correct"]+=1
    return flask.render_template('response.html', 
                                num=num, max_num = max_num, 
                                game_mode=game_mode, response=response,
                                correct=correct)


@APP.route('/form')
def form():
    return flask.render_template('form.html', game_modes=modes.keys())


@APP.route('/start_game', methods = ['POST', 'GET'])
def start_game():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        max_num=form_data["num_questions"]
        session["game_mode"]=form_data["game_mode"]
        session["num"]=1
        session["correct"]=0
        session["max_num"]=form_data["num_questions"]

        return redirect(url_for("question"))


@APP.route('/')
def menu():
    return flask.render_template('menu.html')

if __name__ == '__main__':
    APP.debug=True
    APP.run()