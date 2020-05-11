#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


# Database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Flask routes

@app.route("/")
def welcome():
     return (
         f"Available Routes:<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/date/start_date as YYYY-MM-DD <br/>"
         f"/api/v1.0/date/start date/end date as YYYY-MM-DD"
     )

@app.route("/api/v1.0/stations")
def stn():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precip():
     session = Session(engine)
     results = session.query(measurement.date,measurement.prcp).all()
     session.close()
     measures = []
     for date, prcp in results:
         msrs_dict = {}
         msrs_dict["date"] = date
         msrs_dict["prcp"] = prcp
         measures.append(msrs_dict)

     return jsonify(measures)

@app.route("/api/v1.0/tobs")
def tbs():
    session = Session(engine)
    results = session.query(measurement.tobs).filter(measurement.station=="USC00519281",measurement.date>='2016-08-23 00:00:00').all()
    session.close()
    yr_tobs = list(np.ravel(results))
    return jsonify(yr_tobs)

@app.route('/api/v1.0/date/<start>')
def start_only(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>start).all()
    session.close()
    starts = list(np.ravel(results))
    return jsonify(starts)
    
@app.route('/api/v1.0/date/<start>/<end>')
def start_end(start,end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>start).filter(measurement.date<end).all()
    session.close()
    start_nd = list(np.ravel(results))
    return jsonify(start_nd)

if __name__ == '__main__':
    app.run(debug=True)