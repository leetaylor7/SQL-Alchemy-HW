import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Chris to look into why we get errors when not using the check_same_thread arg
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread':False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"`/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    """This shows the Percipitation Data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of Percipitation 
    Percipication = []
    for results in results:
        percipitation_dict = {}
        percipitation_dict["Date"] = Measurement.date
        percipitation_dict["prcp"] = Measurement.prcp
        Percipitation.append(percipitation_dict)

    return jsonify(Percipitation)

@app.route("/api/v1.0/stations")
def percipitation():
    """This shows the Percipitation Data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of Percipitation 
    all_atations = []
    for results in results:
        station_dict = {}
        station_dict["Stations"] = Measurement.stations
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/<start>&<end>")
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    ranged_data = {
        "TMIN" : results[0],
        "TAVE" : results[1],
        "TMAX" : results[2]
    }
    
    return jsonify(ranged_data)

@app.route("/api/v1.0/<start>")
def start_calc_temp(start_date):
        """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """

    results1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    start_ranged_data = {
        "TMIN" : results1[0],
        "TAVE" : results1[1],
        "TMAX" : results1[2]
    }
    
    return jsonify(start_ranged_data)

@app.route("/api/v1.0/<end>")
def calc_temps(end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= end_date).all()

    end_ranged_data = {
        "TMIN" : results2[0],
        "TAVE" : results2[1],
        "TMAX" : results2[2]
    }
    
    return jsonify(end_ranged_data)