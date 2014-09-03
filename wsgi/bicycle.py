from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


class Station(db.Model):
    __tablename__ = 'stations'
    station_id= db.Column('station_id', db.String, primary_key=True)
    address = db.Column(db.String)
    description = db.Column(db.String)
    available_bicycles = db.Column(db.Integer)
    available_poles = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, station_id, address, description, latitude, longitude, available_bicycles, available_poles, capacity):
        self.station_id = station_id
        self.address = address
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.available_bicycles = available_bicycles
        self.available_poles = available_poles
        self.capacity = capacity
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/new")
def new():
    station = Station("station_id", "Dizingoff 22", "Across the street from whatever", 33.3333, 34.12345, 10, 5, 15)
    db.session.add(station)
    db.session.commit()
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run()

