from db import db, Users, Rides, Bookings
from flask import Flask, request
import json


app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/rideshare/")
def hello_world():
    return ("Hello World")

@app.route("/rideshare/authenticate/", methods = ["POST"])
def create_user():
    """
    End point to create and authenticate email address of both old and new users
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    first_name = body.get("first_name")
    last_name = body.get("last_name")
    # Check if all required fields are present
    if None in (username, password, first_name, last_name):
        return failure_response("Missing a field",400)
    
    # authenticating username
    if not username.lower().endswith("@cornell.edu"):
         return failure_response("Invalid username",400)
    
    #checking if a user already exist 
    user = Users.query.filter_by(username=username).first()
    if not user is None:
        return failure_response("User already exist",400)
    
    #creating a new user if it doesn't exist
    new_user = Users(username = username, password=password,
                    first_name=first_name,last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(),201)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
