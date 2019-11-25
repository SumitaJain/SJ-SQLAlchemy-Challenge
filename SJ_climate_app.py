import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

# Route 1

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Route 2

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query last year of precipitation data 
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    latest_prcp = list(np.ravel(prcp_results))

    return jsonify(latest_prcp)

# Route 3

@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    stations_results = session.query(Station.station).all()
    session.close
    stations_list = list(np.ravel(stations_results))
    return jsonify(stations_list)

# Route 4

@app.route("/api/v1.0/tobs")

def tobs():
    session = Session(engine)
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    session.close
    tobs_list = list(np.ravel(tobs_results))
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)
