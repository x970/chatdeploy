import pyrebase

config = {
    "apiKey": "AIzaSyBktUn36xLC9xvfyrLmYAn8-MGZ1MVCjAc",
    "authDomain": "chatbot-e4397.firebaseapp.com",
    "databaseURL": "https://chatbot-e4397.firebaseio.com",
    "projectId": "chatbot-e4397",
    "storageBucket": "chatbot-e4397.appspot.com",
    "messagingSenderId": "289196394448",
    "appId": "1:289196394448:web:1b806d2b6a1c52b5d71bd5",
    "measurementId": "G-S2X4YZGJZD"
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
