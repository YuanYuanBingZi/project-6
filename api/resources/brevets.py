"""
Resource: BrevetsResource
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

class BrevetsResource(Resource):
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        ## Because input_json is a dictionary, we can do this:
        #brevet_dist = input_json["brevet_dist"] 
        #start_time = input_json["items"] 
        #controls = input_json["controls"] # Should be a list of dictionaries
        #result = Brevet(brevet_dist=brevet_dist, start_time=start_time, controls=controls).save()

        result = Brevet(**input_json).save()
        return {'_id': str(result.id)}, 200
