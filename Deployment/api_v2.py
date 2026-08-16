#!/usr/bin/env python
# coding: utf-8

# import statements
from fastapi import FastAPI, HTTPException
import json
import numpy as np
import pickle
import datetime

# import the airport encodings file
f = open('airport_encodings.json')
 
# returns json object as a dictionary
airports = json.load(f)

def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    create_airport_encoding is a function that creates an array the length of all arrival airports from the chosen
    departure aiport.  The array consists of all zeros except for the specified arrival airport, which is a 1.  

    Parameters
    ----------
    airport : str
        The specified arrival airport code as a string
    airports: dict
        A dictionary containing all of the arrival airport codes served from the chosen departure airport
        
    Returns
    -------
    np.array
        A NumPy array the length of the number of arrival airports.  All zeros except for a single 1 
        denoting the arrival airport.  Returns None if arrival airport is not found in the input list.
        This is a one-hot encoded airport array.
    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None

# load the final model
with open('finalized_model.pkl', 'rb') as final_model_file:
    model = pickle.load(final_model_file)

def predict_delay(dep_airport, arr_airport, dep_time, arr_time):
    # get one-hot encoded airport for arrival
    encoded_airport = create_airport_encoding(arr_airport, airports)
    print(f'Encoded airport for "{arr_airport}": {encoded_airport}')
    if encoded_airport is None:
        raise HTTPException(status_code = 404, detail = 'Arrival airport not found.')
    
    # convert time to seconds since midnight
    try:
        dep_time_seconds = (datetime.datetime.strptime(dep_time, '%Y-%m-%dT%H:%M:%S') - datetime.datetime(1900, 1, 1)).total_seconds()
        arr_time_seconds = (datetime.datetime.strptime(arr_time, '%Y-%m-%dT%H:%M:%S') - datetime.datetime(1900, 1, 1)).total_seconds()
    except ValueError:
        raise HTTPException(status_code = 400, detail = 'Invalid time format. Time must be "YYYY-MM-DDTHH:MM:SS".')

    # prepare the input array with polynomial order, length of airports, departure seconds since midnight, arrival seconds since midnight
    input_data = np.concatenate(([1], encoded_airport, [dep_time_seconds], [arr_time_seconds]))
    
    # prediction
    delay = model.predict(input_data.reshape(1, -1))  # needed since the model expects a 2D array
    
    return delay[0]

# initialize fastapi app
app = FastAPI()

# root endpoint to verify api is functional
@app.get('/')
async def root():
    return {'message': 'API is functional.'}

# prediction endpoint to get average departure delay
@app.get('/predict/delays')
async def predict_delays(arr_airport: str, dep_airport: str, dep_time: str, arr_time: str):
    try:
        delay = predict_delay(dep_airport, arr_airport, dep_time, arr_time)
        return {'Average Departure Delay': delay}
    except HTTPException as e:
        raise e