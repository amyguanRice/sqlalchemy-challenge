import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
stations = Base.classes.station

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
        f"Welcome to my 'Home' page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date, station, and precipitation"""
    # Query all passengers
    results = session.query(measurement.station, measurement.date, measurement.prcp).all()

    session.close()
   

    # Create a dictionary from the row data and append to a list 
    Precipitation = []
    for station, date, prcp in results:
        precipitation_dict = {date:prcp}
        Precipitation.append(precipitation_dict)

    return jsonify(Precipitation)


@app.route("/api/v1.0/stations")
def stats():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date, station, and precipitation"""
    # Query all passengers
    results = session.query(stations.station).all()

    session.close()
   

    # Create a dictionary from the row data and append to a list 
    Stations = []
    # for station in results:
    station_dict={}
    #     Station_dict['station'] = station
    #     Stations.append(Station_dict)
    station_dict['station'] = list(np.ravel(results))
    Stations.append(station_dict)
    return jsonify(Stations)


@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including the date, station, and precipitation"""
    
    # Query all temp from the last year for station #519281
    
    results_tobs = session.query(measurement.tobs).\
        filter(measurement.date>dt.datetime(2016,8,23)).\
        filter(measurement.station=='USC00519281').all()

    results_date = session.query(measurement.date).\
        filter(measurement.date>dt.datetime(2016,8,23)).\
        filter(measurement.station=='USC00519281').all()

    session.close()
   
    # Create a dictionary from the row data and append to a list 
    Temperature = []
    # for station in results:
    temp_dict={}
    temp_dict['tobs'] = list(np.ravel(results_tobs))
    temp_dict['date'] = list(np.ravel(results_date))
    # temp_dict = list(np.ravel(results))
    Temperature.append(temp_dict)

    return jsonify(Temperature)


@app.route("/api/v1.0/<start>")
def T_Stats(start):

    try:
        val = input("Please enter the start date in the foramt of YYYY-MM-DD : ")
        start_year = int(val[:4])
        start_month = int(val[5:7])
        start_day = int(val[8:])

        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of precipitation data including the date, station, and precipitation"""
        
        results_tobs = session.query(measurement.tobs).\
            filter(measurement.date>=dt.datetime(start_year,start_month,start_day)).\
            filter(measurement.station=='USC00519281').all()

        session.close()
    
        # Create a dictionary from the row data and append to a list 
        Temperature = []
        temp_dict={}
        temp_dict['TMIN'] = min(list(np.ravel(results_tobs)))
        temp_dict['TAVG'] = np.average(list(np.ravel(results_tobs)))
        temp_dict['TMAX'] = max(list(np.ravel(results_tobs)))
        Temperature.append(temp_dict)

        return jsonify(Temperature)

    except:
        return(f"Please make sure your date format is an exact match to YYYY-MM-DD.<br/>"
        f"Refresh to reload your webpage!")


@app.route("/api/v1.0/<start>/<end>")
def T_Stats_start_end(start,end):

    try:
        val = input("Please enter the start date in the foramt of YYYY-MM-DD : ")
        start_year = int(val[:4])
        start_month = int(val[5:7])
        start_day = int(val[8:])

        val1 = input("Please enter the end date in the foramt of YYYY-MM-DD : ")
        end_year = int(val1[:4])
        end_month = int(val1[5:7])
        end_day = int(val1[8:])

        # Create our session (link) from Python to the DB
        session = Session(engine)

        """Return a list of precipitation data including the date, station, and precipitation"""
        
        results_tobs = session.query(measurement.tobs).\
            filter(measurement.date>=dt.datetime(start_year,start_month,start_day)).\
            filter(measurement.date<=dt.datetime(end_year,end_month,end_day)).\
            filter(measurement.station=='USC00519281').all()

        session.close()
    
        # Create a dictionary from the row data and append to a list 
        Temperature = []
        temp_dict={}
        temp_dict['TMIN'] = min(list(np.ravel(results_tobs)))
        temp_dict['TAVG'] = np.average(list(np.ravel(results_tobs)))
        temp_dict['TMAX'] = max(list(np.ravel(results_tobs)))
        Temperature.append(temp_dict)

        return jsonify(Temperature)

    except:
        return(f"Please make sure your date format is an exact match to YYYY-MM-DD.<br/>"
        f"And also your request does not fall out of the date range of Jan, 2010 and Aug 23, 2017.<br/>"
        f"If your range starts earlier than Jan,2010, or ends later than Aug 23, 2017, please beaware of the actual range!<br/>"
        f"Refresh to reload your webpage!")

        
if __name__ == '__main__':
    app.run(debug=True)
