from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import datetime

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model,SerializerMixin):
    __tablename__ = "customers"
    
    # id = db.Column(db.Integer, primary_key=True) 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    reservation = db.relationship('Reservation' , back_populates='customer')
    
    serialize_rules = ('-reservation.customer',)
    locations = association_proxy('reservation', 'location')
    
    # validates customers.name
    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError('What df dawg?')
        return name
    
    # valiates customers.email
    @validates('email')
    def vaidates_email(self, key, email):
        if '@' not in email:
            raise ValueError('What is this you jamoke?')
        return email 
        


class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"
    
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    max_party_size = db.Column(db.Integer, nullable=False)
    
    # bidimensional relationship 
    reservation = db.relationship('Reservation' ,back_populates='location')
    customers = association_proxy('reservation', 'customer')
    serialize_rules = ('-reservation.location',)
    
    # validates locations.name
    @validates('name')
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError('What df dawg?')
        return name
    
    # validates max_party_size
    @validates('max_party_size')
    def validates_max_party_size(self, key, max_party_size):
        if not max_party_size and not isinstance(max_party_size, int):
            raise ValueError('gahdamn where the people at?')
        return max_party_size

class Reservation(db.Model, SerializerMixin):
    __tablename__ = "reservations"
    # custy cant have more than 1 reservation for same date and location
    __table_args__ = (UniqueConstraint(
        "location_id", "customer_id", "reservation_date"),)
    
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String, nullable=False)
    party_size = db.Column(db.Integer)
    reservation_date = db.Column(db.Date, nullable=False)
    
    # bidimensional relationship 
    # needed to use db.Integer in this case, for some reason 'Classname' != working
    location_id = db.Column(db.Integer, ForeignKey('locations.id'), nullable=False)
    location = db.relationship('Location', back_populates='reservation')
    customer_id = db.Column(db.Integer, ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='reservation')
    
    # know when and why to implement them
    serialize_rules = ('-location.reservation', "-customer.reservation")
    
    # nullable and @validaties 
    # db.func.now() (takes local time from machine)
    
    # validates reservations.date
    @validates('reservation_date')
    def validate_date(self, key, reservation_date):
        if not isinstance(reservation_date, datetime.date):
            raise TypeError('must be a valid date')
        return reservation_date
    
    # # validates reservations.party_name
    @validates('party_name')
    def validates_party_name(self, key, party_name):
        if not party_name or len(party_name) < 1:
            raise ValueError('What the name is Babyboy?')
        return party_name
    
    # # validates reservations.customer_id
    @validates('customer_id')
    def validates_customerID(self, key, customer_id):
    # could use setattr or isinstance
        if not customer_id and not isinstance(customer_id, int):
            raise ValueError("where them id's at?")
        return customer_id
    
    # # validates reservations.location_id
    @validates('location_id')
    def validates_location_id(self, key, location_id):
        if not location_id and not isinstance(location_id, int):
            raise ValueError('What are you doing mane? ')
        return location_id