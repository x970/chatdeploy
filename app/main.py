from flask import Flask, jsonify, request, make_response
from typing import Dict, Any

from app.src import medbot as medbotrefactored
import uuid
import time
import json
import datetime
import pyrebase
from flask_cors import CORS
import re

config = {
    "apiKey": "AIzaSyA1cwRdlql8imfzRWdJOdtOzNEpW_r2po4",
    "authDomain": "chatbot-2071e.firebaseapp.com",
    "databaseURL": "https://chatbot-2071e.firebaseio.com",
    "projectId": "chatbot-2071e",
    "storageBucket": "chatbot-2071e.appspot.com",
    "messagingSenderId": "939444021333",
    "appId": "1:939444021333:web:07396d4b7326bbffa10cdc"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def insert_user(uuid):
    data = {"name": "", "stage": "greeting", "age": "", "gender": "", "choice": "", "symptoms": "", "diagnosis": "",
            "score": ""}
    db.child("users").child(uuid).set(data)


def update_name(uuid, name):
    data = {"name": name, "stage": "name"}
    db.child("users").child(uuid).update(data)


def update_age(uuid, age):
    data = {"age": age, "stage": "age"}
    db.child("users").child(uuid).update(data)


def update_gender(uuid, gender):
    data = {"gender": gender, "stage": "gender"}
    db.child("users").child(uuid).update(data)


def update_choice(uuid, choice):
    data = {"choice": choice, "stage": "choice"}
    db.child("users").child(uuid).update(data)


def update_symptoms(uuid, symptoms):
    data = {"symptoms": symptoms, "stage": "symptoms"}
    db.child("users").child(uuid).update(data)


def update_diagnosis(uuid, diagnosis):
    data = {"diagnosis": diagnosis, "stage": "diagnosis"}
    db.child("users").child(uuid).update(data)


def update_score(uuid, score):
    data = {"score": score, "stage": "diagnosis"}
    db.child("users").child(uuid).update(data)


def get_stage(uuid):
    stage = db.child("users").child(uuid).child("stage").get()
    return stage.val()


def update_stage(uuid, stage):
    data = {"stage": stage}
    db.child("users").child(uuid).update(data)


def get_name(uuid):
    name = db.child("users").child(uuid).child("name").get()
    return name.val()

#1 check name Function
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

app = Flask(__name__)
CORS(app,supports_credentials=True,resources={
    r"/medbot": {"origins":"*"}
})

'''CORS'(app,supports_credentials=True,resources={
    r"/logout": {"origins":"*"}
})'''

class Response:
    def __init__(self):
        pass

    @classmethod
    def send(cls, response_message: Dict[str, Any], status_code: int):
        response = make_response(json.dumps(response_message))

        #response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5000/medbot")
        #response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['mimetype'] = 'application/json'
        #response.headers['Access-Control-Allow-Origin'] = '*'
        response.status_code = status_code

        return response


def initialize_user():
    user_id = f"{str(int(time.time()))}-{str(uuid.uuid4())}"
    insert_user(user_id)

    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=15)

    message = {'message':  medbotrefactored.greet()}

    response = Response.send(message, 200)
    response.set_cookie('uuid', user_id, expires=expire_date)
    return response


# Globals
restart_process = False

'''@app.route("/logout", methods=['POST'])
def Logout_User():
    message = {'message': 'Goodbye'}
    response = Response.send(message, 200)
    response.set_cookie('uuid', '', expires=0)
    return response'''

@app.route("/medbot", methods=['POST'])
def initialize_chat():
    user_id = request.cookies.get('uuid')
    stage = get_stage(user_id)
    global restart_process

    if not stage:
        restart_process = False
        return initialize_user()
    elif stage == 'symptoms':  #new
        message = {'message': medbotrefactored.greet(user_id)}
        update_stage(user_id, 'greeting')

        restart_process = True

        return Response.send(message, 200)
    #2 when user refresh page that return this message and current stage
    if request.get_data() == b'':
        message = ""
        if stage == "choice":
            message = {'message':  ['Please enter you name']}
            return Response.send(message, 200)
        elif stage == 'name':
            message = {'message':  ['Please enter your age']}
            return Response.send(message, 200)
        elif stage == 'age':
            message = {'message':  ['Please enter your gender (male or female)']}
            return Response.send(message, 200)
        elif stage == 'gender':
            message = {'message':  ['Please enter your symptoms']}
            return Response.send(message, 200)
        elif stage == 'greeting':
            # TDB
            message = {'message': medbotrefactored.greet(user_id)}
            return Response.send(message, 200)
        else:
            message = {'message':  ['Unknown stage']}
            return Response.send(message, 200)

    if stage == 'greeting':
        reqbody = request.get_json(force=True)
        choice = reqbody['input']

        if choice == "1":
            update_choice(user_id, choice)
            #when user come back to use medbot
            if restart_process:
                message = {'message': medbotrefactored.ask_symptoms()}
                update_stage(user_id, 'gender')
                return Response.send(message, 200)

            message = {'message':  medbotrefactored.asknames()}
            return Response.send(message, 200)
        #when select two take user to Book intensive care unit
        if choice == "2":
            message = {'message': ['Your request has been executed']}
            response = Response.send(message, 200)
            response.set_cookie('uuid', '', expires=0)

            return response

        else:
            message = {'message': ['Please enter valid choice']}

            return Response.send(message, 200)

    if stage == 'choice':
        reqbody = request.get_json(force=True)
        name = reqbody['input']
        if hasNumbers(name): #continue 1 no enter integer
            message = {'message': ['Please enter valid name']}
            return Response.send(message, 200)
        else: #3 when user enter iam then here delet it from message
            name = name.replace("I am ", "").replace("my name is", "").replace("my name ","").replace("iam ","").replace("i'm ","")
            update_name(user_id, name)
            message = {'message': medbotrefactored.askAges(user_id)}
            return Response.send(message, 200)

    if stage == 'name':
        reqbody = request.get_json(force=True)
        age = reqbody['input']


        if hasNumbers(age): #1 continue if user enter string not number or int
            age = str(int(re.search(r'\d+', age).group()))
            update_age(user_id, age)
            message = {'message': medbotrefactored.getAge(user_id, age)}
            return Response.send(message, 200)
        else:

            message = {'message':['Please enter valid age']}
            return Response.send(message, 200)

    if stage == 'age':
        reqbody = request.get_json(force=True)
        gender = reqbody['input']

        if medbotrefactored.getGender(gender) != 0:
            update_gender(user_id, gender)
            message = {'message': medbotrefactored.ask_symptoms()}
            return Response.send(message, 200)

        else:
            message = {'message': medbotrefactored.sorry()}
            return Response.send(message, 200)

    if stage == 'gender':
        reqbody = request.get_json(force=True)
        symptoms = reqbody['input']
        res = medbotrefactored.getdisease(symptoms)
        print(res)
        if res == "0":
            message = {'message': ['Please enter valid symptoms']}
            return Response.send(message, 200)
        else:
            message = {'message': res}
            update_symptoms(user_id, symptoms)

            return Response.send(message, 200)
