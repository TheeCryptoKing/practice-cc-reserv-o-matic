import pytest
from app import app
from sqlalchemy.exc import IntegrityError
import datetime
from models import db, Customer, Location, Reservation


class TestModels:
    """SQLAlchemy models in models.py"""

    def test_validates_customer_name(self):
        """require customers to have names."""

        with app.app_context():
            with pytest.raises(ValueError):
                Customer(name=None, email="steve@aol.com")

            with pytest.raises(ValueError):
                Customer(name="", email="steve@aol.com")

    def test_validates_customer_email(self):
        """require customers to have an email."""
        with app.app_context():
            with pytest.raises(ValueError):
                Customer(name="Ben", email="")

            with pytest.raises(ValueError):
                Customer(name="Steve", email="johnjacob")

    def test_validates_reservation_customer(self):
        """requires reservations to have a customer."""
        with app.app_context():
            res = Reservation(
                reservation_date=datetime.date(2023, 6, 19),
                # customer_id=1,
                location_id=1,
                party_size=4,
                party_name="spider friends",
            )
            with pytest.raises(IntegrityError):
                db.session.add(res)
                db.session.commit()

    def test_validates_reservation_location(self):
        """requires reservations to have a location."""
        with app.app_context():
            res = Reservation(
                reservation_date=datetime.date(2023, 6, 19),
                customer_id=1,
                # location_id=1,
                party_size=4,
                party_name="spider friends",
            )
            with pytest.raises(IntegrityError):
                db.session.add(res)
                db.session.commit()

    def test_validates_reservation_date(self):
        """requires reservations to have a valid date."""
        with app.app_context():
            with pytest.raises(TypeError):
                Reservation(
                    reservation_date="2023-06-19",
                    customer_id=1,
                    location_id=1,
                    party_size=4,
                    party_name="spider friends",
                )

    def test_validates_reservation_party_size(self):
        """requires reservations to have a valid party name."""
        with app.app_context():
            res = Reservation(
                reservation_date=datetime.date(2023, 6, 19),
                customer_id=1,
                location_id=1,
                party_size=5,
                # party_name="spider friends",
            )
            with pytest.raises(ValueError):
                db.session.add(res)
                db.session.commit()
