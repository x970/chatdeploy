import pyrebase

config = {
    "apiKey": "AIzaSyDqANnC3QfNhGNDl3XY5Ex9rT4EfRFstVY",
    "authDomain": "project-bb940.firebaseapp.com",
    "databaseURL": "https://project-bb940.firebaseio.com",
    "projectId": "project-bb940",
    "storageBucket": "project-bb940.appspot.com",
    "messagingSenderId": "1042006402675",
    "appId": "1:1042006402675:web:edddc41d1d7ea5f9adac06",
    "measurementId": "G-F0VP8LCC9Z"
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
