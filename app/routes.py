
# Imports
from app import app
from flask import request
import flask
import json
import sys
sys.path.append('./database')
from db_utils import create_connection
sys.path.append('./app')
from activities import GatherActivities
from hostels import gatherHostelData

# Potentially useful imports:
#from app.trains import GatherTrains

@app.route('/')
def home():
    return "Server is running"


@app.route('/cities')
def getCitiesOverview():

    # Database query
    conn = create_connection('./database/Wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT id,name,country,population,latitude,longitude FROM cities'
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()

    # Format response
    cities = []
    for entry in data:
        city = {'name': entry[1], 'city_id': entry[0], 'country': entry[2], 'population': entry[3], 
                'latitude': entry[4], 'longitude': entry[5]}
        cities.append(city)
    
    response = flask.jsonify(cities)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/city_info/<cid>')
def getCityInfo(cid):
    
    # Database query
    conn = create_connection('./database/Wanderweg.db')
    cur = conn.cursor()
    sql = 'SELECT name,country,hostel_url,weather FROM cities WHERE id=' + cid
    cur.execute(sql)
    data = cur.fetchone()
    conn.close()

    # Fetch activities
    # TO DO: should we include country in acitivities search? Could help for when we scale
    activityScraper = GatherActivities()
    activities = activityScraper.scrapeCity(data[0])

    data = list(data)
    print(type(data), data)
    data.append(activities)
   
    # Fetch hostel info
    hostelData = gatherHostelData(data[2])

    # Format response
    info = {'activities': activities, 'hostels': hostelData}
    response = flask.jsonify(info)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Use params or something to accept a list of destinations
@app.route('/travel', methods=['GET'])
def createTravelPlan():
    return "TODO"

"""
Saved these two routes because they could be usefull for helper function for our final routes.
#Returns activities in a city
@app.route('/activities/<city>')
def getActivities(city):
    activityScraper = GatherActivities()
    return activityScraper.scrapeCity(city)

#Returns train info for a trip between two cities 
#Note that requests need to replace spaces with underscores
@app.route('/trains', methods=['GET'])
def getTrains():
    #Fetch and clean up params
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    num_results = int(request.args.get('n'))
    origin = origin.replace("_", " ")
    destination = destination.replace("_", " ")
    #Get route data
    trainScraper = GatherTrains()
    return trainScraper.scrapeAllInfo(origin, destination, date, num_results)

"""