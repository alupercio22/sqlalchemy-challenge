#import
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
#home page
#list all routes that are available
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )
#precipitation
#convert the query results to a dictionary using date as they key & prcp as the value
#return the JSON representaiton of your dictionary
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create session (link)
    session = Session(engine)
    """Return a list of all precipitation data"""
    #Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()
    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))
    # Convert the list to Dictionary
    all_precipitation = {all_precipitation[i]: all_precipitation[i + 1] for i in range(0, len(all_precipitation), 2)}
    return jsonify(all_precipitation)

#stations
#return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all Stations"""
    results = session.query(Station.station).order_by(Station.station).all()

    session.close()
#TOBS
#query the dates and temperature observations of the most active stations for the last year of date
#return a JSON lisst of temperature observations (TOBS) for the previous year
@app.route('/api/v1.0/tobs')
def TOBS():
    session = Session(engine)
    """Return a list of all TOBS"""
    results = session.query(Measurement.date,Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >='2016-08-23').\
                filter(Measurement.
                station=='USC00519281').\
                order_by(Measurement.date).all()
    
    session.close()

    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict['prcp'] = prcp
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

#JSON
@app.route('/api/v1.0/<start>')
def JSON():
    session = Session(engine)

    """Return a list of min, avg and max TOBS for a start date"""

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
session.close()
start_date_tobs = []
for min, avg, max in results:
    start_date_tobs_dict = {}
    start_date_tobs_dict['min_temp'] = min
    start_date_tobs_dict['avg_temp'] = avg
    start_date_tobs_dict['max_temp'] = max
    start_date_tobs.append(start_date_tobs_dict)

return jsonify(start_date_tobs)

#json2



#4. define main behavior
if name == 'main':
    app.run(debug=True)