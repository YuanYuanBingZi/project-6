"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import requests
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import logging

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def get_brevet():
    """
    Obtains the newest document in the lists collection in database
    by calling the RESTful API.
    Returns brev_dist, start_time, controls (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = requests.get(f"{API_URL}/brevets").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    list = lists[-1]
    return list["brevet_dist"], list["start_time"], list["controls"]

def insert_brevet(brevet_dist, start_time, controls):
    """
    Inserts a new brevet into the database by calling the API.
    
    Inputs a brevet_dist, start_time  and controls (list of dictionaries).
    """
    _id = requests.post(f"{API_URL}/brevets", json={"brevet_dist": brevet_dist, "start_time": start_time, "controls": controls}).json()
    return _id

##################################################
################## Flask routes ################## 
##################################################

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    distance = request.args.get('distance',type=float)
    temp = request.args.get('start_time',type=str)
    start_time = arrow.get(temp, 'YYYY-MM-DDTHH:mm')
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, distance, start_time).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

@app.route("/insert", methods = ["POST"])
def insert():
    input_json = request.json
    brevet_dist = input_json["brevet_dist"]
    start_time = input_json["start_time"]
    controls = input_json["controls"]
        
    brevet_id = insert_brevet(brevet_dist, start_time, controls)
    return flask.jsonify(result = {}, message = "Inserted!", status = 1, mongo_id = brevet_id) 


@app.route("/fetch")
def fetch():
    brevet_dist, start_time, controls = get_brevet()
    return flask.jsonify(
            result={"brevet_dist": brevet_dist, "start_time": start_time, "controls": controls}, 
            status=1,
            message="Successfully fetched one brevet row!")

##################################################
################# Start Flask App ################ 
##################################################

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
