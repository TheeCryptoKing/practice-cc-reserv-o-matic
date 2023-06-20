#!/usr/bin/env python3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite://{os.path.join(BASE_DIR, 'instance/app.db')}"
# )

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Customer, Location, Reservation
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance/app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def home():
    return ""

# Customers, Locations, Reservations 
class Customers(Resource):
    # GET, POST

    def get(self):
        custyData = [custy.to_dict() for custy in Customer.query.all()]
        return custyData, 200 
    
    def post(self):
        print('Custy Post intiating...')
        data = request.get_json()
        try:
            newCustomer = Customer(
                name=data.get('name'),
                email=data.get('email')
            )
            db.session.add(newCustomer)
            db.session.commit()
            return newCustomer.to_dict(), 201
        
        except:
            return {"error": "404: Customer not found"}, 400
api.add_resource(Customers, '/customers')

class CustomersId(Resource):
    # GET
    def get(self, id):
        try:
            custyById = Customer.query.filter_by(id=id).first().to_dict()
            return custyById, 200
        except:
            return {"error": "404: Customer not found"}, 404

api.add_resource(CustomersId,'/customers/<int:id>')

class Locations(Resource):
    # GET
    def get(self):
        locateData = [location.to_dict() for location in Location.query.all()]
        return locateData, 200
    
api.add_resource(Locations, '/locations')

class Reservations(Resource):
    # POST
    
    # check data in endpoint
    def get(self):
        reservations = [reservation.to_dict() for reservation in Reservation.query.all()]
        return reservations, 200
    
    def post(self):
        print('Resey Post initiating...')
        try:
            data = request.get_json()
            newReservation = Reservation(
                reservation_date=datetime.datetime.strptime(data.get('reservation_date'),"%Y-%m-%d").date(),
                customer_id=data.get('customer_id'),
                location_id=data.get('location_id'),
                party_size=data.get('party_size'),
                party_name=data.get('party_name')
            )
            db.session.add(newReservation)
            db.session.commit()
            return newReservation.to_dict(), 201
        
        except:
            return ({"error": "400: Validation error"}, 400)
        
api.add_resource(Reservations, '/reservations')

class ReservationsId(Resource):
    # PATCH, DELETE
    
    # check to see data in endpoint
    def get(self):
        reservation = Reservation.query.filter(Reservation.id == id).first().to_dict()
        return reservation, 200
    
    def patch(self, id):
        print('Resey patch intiating...')
        data = request.get_json()
        resey = Reservation.query.filter(Reservation.id == id).first()
        if not resey:
            return ({"error" : "404: Reservation not found"}, 404)
        for r in data:
            print(r, data)
            if r == "reservation_date":
                setattr(
                    resey,
                    r,
                    datetime.datetime.strptime(
                        data.get("reservation_date"),"%Y-%m-%d"
                    ).date(),
                )
            else: 
                setattr(resey, r, data.get(r))
        try:
            db.session.add(resey)
            db.session.commit()
            return resey.to_dict(), 200 
        except Exception:
            return ({"error" : "404 not found"}, 400)

    
    def delete(self, id):
        print('Resey delete intiating...')
        try:
            resey = Reservation.query.filter(Reservation.id == id).first()
            db.session.delete(resey)
            db.session.commit()
            return ({}, 204)
        except:
            return ({"error": "404: Reservation not found"}, 404)
        
api.add_resource(ReservationsId, '/reservations/<int:id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    
    
    
    # Takeaways
    # Practice more patchs
    # Practice serialization_rules, valiadte methods, uniqueConstraints
    # find out when foreignkey needs a Integer and Class
    # play with serialization to get data outputing properly 
    
