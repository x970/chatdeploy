import pyrebase

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


def get_name(uuid):
    name = db.child("users").child(uuid).child("name").get()
    return name.val()
