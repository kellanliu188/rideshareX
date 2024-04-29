from db import db, Users, Rides, Bookings
from flask import Flask, request
import json
import re
from datetime import datetime


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

@app.route("/rideshare/rides/")
def get_all_rides():
    """
    End point for get all the courses
    """
    return success_response({"rides": [
        rides.serialize() for rides in Rides.query.all()
    ]})

@app.route("/rideshare/rides/<int:ride_id>/")
def get_specific_ride(ride_id):
    """
    End point for getting specific rides
    """

    ride = Rides.query.filter_by(ride_id = ride_id).first()
    if ride is None:
        return failure_response("Ride not found")
    return success_response(ride.serialize())

#
@app.route("/rideshare/addtrip/<int:driver_id>/", methods = ["POST"])
def add_ride(driver_id):
    """
    add a trip
    """
    body = json.loads(request.data)
    if "origin" not in body or "destination" not in body or "departure_time" not in body or "available_seats" not in body:
        return failure_response("Missing input", 400)
    origin = body.get("origin")
    destination = body.get("destination")
    departure_time = body.get("departure_time")
    available_seats = body.get("available_seats")

    if type(origin) is not str or type(destination) is not str or type(available_seats) is not int or type(departure_time) is not str :
        return failure_response("Incorrect input type", 400)
    
    try:
        date_time_obj = datetime.strptime(departure_time, '%m-%d-%y %H:%M')
    except ValueError:
        return failure_response("The date and time are not valid.", 400)
    
    new_ride = Rides(driver_id = driver_id, origin=origin, destination=destination, departure_time=departure_time, available_seats=available_seats)
    db.session.add(new_ride)
    db.session.commit()
    return success_response(new_ride.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
