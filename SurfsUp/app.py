#import modules & dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#connect to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect database
Base = automap_base()
Base.prepare(autoload_with=engine)
#reference to table
measurement = Base.classes.measurement
station = Base.classes.station
#setup Flask
app = Flask(__name__)

#setup routes
@app.route("/")
def welcom():
    """Welcome to the Hawaii Weather Station Report."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Attention: to set start and end date enter both dates in YYYY-MM-DD/YYYY-MM-DD format"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session to link from Python to the database
    session=Session(engine)
    """Return daily precipitation totals for the last year"""
    #create variable to store query results for precipitation totals for the last year
    starting_date = "2016-08-23"
    sel = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >="2016-08-23").\
        all()
    session.close()
    
    #convert to dict, convert from dict to json
    prcp_amounts = []
    for date, prcp in sel:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        prcp_amounts.append(prcp_dict)
    return jsonify(prcp_amounts)
    
@app.route("/api/v1.0/stations")
def stations():
    #create session to link from Python to the database
    session=Session(engine)
    """Return list of all stations in dataset"""
    sel = session.query(station.station).\
        order_by(station.station).all()
    session.close()
    
    #convert from dict. to jsonified list
    station_list = list(np.ravel(sel))
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    #create session to link from Python to the database
    session=Session(engine)
    """Return temps for the most-active station for the pervious year in dataset"""
    sel=session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        filter(measurement.station=="USC00519281").\
        order_by(measurement.date).all()
    session.close()
    
    #convert from dict. to jsonified list
    comp_tobs = []
    for prcp, date, tobs in sel:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        comp_tobs.append(tobs_dict)
    return jsonify(comp_tobs)
    
@app.route("/api/v1.0/<start>")
def Start_date(start_date):
    #create session to link from Python to the database
    session=Session(engine)
    """Return min, avg, and max temp for single start date"""
    sel = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()
        
    start_date_data = []
    for min, avg, max in sel:
        start_date_dict = {}
        start_date_dict["Min"] = min
        start_date_dict["Avg"] = avg
        start_date_dict["Max"] = max
        start_date_data.append(start_date_dict)
        
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    #create session to link from Python to the database
    session=Session(engine)
    """Return min, avg, and max temp for range of dates for start and end date"""
    sel = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()
    
    start_end_date_data = []
    for min, avg, max in sel:
        start_end_date_dict = {}
        start_end_date_dict["Min"] = min
        start_end_date_dict["Avg"] = avg
        start_end_date_dict["Max"] = max
        start_end_date_data.append(start_end_date_dict)
        
    return jsonify(start_end_date_data)
        
if __name__ == "__main__":
    app.run(debug=True)
        
        
        
    
    
