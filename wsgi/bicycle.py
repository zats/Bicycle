import datetime
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

    def __init__(self, station_id, address, description, available_bicycles, available_poles, capacity):
        self.station_id = station_id
        self.address = address
        self.description = description
        self.available_bicycles = available_bicycles
        self.available_poles = available_poles
        self.capacity = capacity
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/env")
def env():
    return ""

if __name__ == "__main__":
    app.run()

