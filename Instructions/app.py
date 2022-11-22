import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station


app = Flask(__name__)
@app.route("/")
def welcome():
    session = Session(engine)
    session.close()
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    dates = dt.date(2017,8,23) - dt.timedelta(days=365)
    data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= dates).all()
    session.close()
    precip = []
    for date, prcp in data:
        prcpdict = {}
        prcpdict["date"] = date
        prcpdict["prcp"] = prcp
        precip.append(prcpdict)
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stat = session.query(station.station).all()
    session.close()
    allstations = list(np.ravel(stat))
    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    dates = dt.date(2017,8,23) - dt.timedelta(days=365)
    d = session.query(measurement.tobs).filter(measurement.date >= dates).filter(measurement.station == 'USC00519281').all()
    session.close()
    temp = list(np.ravel(d))
    return jsonify(temp)

# no idea how to do this part
@app.route("/api/v1.0/temp/<start>")
def startdate(start):
    session = Session(engine)
    temp = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start)
    session.close()
    stlist = list(np.ravel(temp))
    return jsonify(stlist)

@app.route("/api/v1.0/<start>/<end>")
def startend(start=None,end=None):
    session = Session(engine)
    temps = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    tlist = list(np.ravel(temps))
    return jsonify(tlist)


if __name__ == '__main__':
    app.run(debug=True)