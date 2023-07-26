import json
from flask import Blueprint, request, redirect, make_response, jsonify
import requests
import os
import pandas as pd

from objects.address import Address
from objects.point_of_interest import PointOfInterest
from objects.poi_list import PoiList
from db.poi_dao import PoiDao
from objects.position import Position

poi = Blueprint('poi', __name__, url_prefix='/pois')
poi_dao = PoiDao()


@poi.route("/", methods=["GET", "POST"])
def poi_collection_manager():
    if request.method == "GET":
        args = request.args.to_dict()
        if args.get( 'sort_by', None ) is not None:
            sort_by = args.pop( 'sort_by' )
            direction = -1 if sort_by[0] == '-' else 1
            sort_by = sort_by[1:]
        else:
            sort_by = None
            direction = 0
        # between is the parameter used as filter for the range
        # start and and could be empty and the respective condition will not be set.
        if args.get( 'between', None ) is not None and (
                args.get( 'start', None ) is not None or args.get( 'end', None ) is not None):
            start = args.pop( 'start', None )
            end = args.pop( 'end', None )
            return json.dumps(
                poi_dao.get_hotels_by_range( parameter=args['between'], start=start, end=end, sort_by=sort_by,
                                               direction=direction ).to_json() )
        return json.dumps( poi_dao.get_pois( parameters=args, sort_by=sort_by, direction=direction ).to_json() )
    elif request.method == "POST":
        print(request.json)
        poi = PointOfInterest.dict_to_cls(json.loads(request.json))
        if not poi_dao.add_poi(poi):
            res = make_response(jsonify({"error": "Point of interest already exists"}), 400)
            return res
        res = make_response(jsonify({"message": "Point of interest created"}), 201)
        return res


@poi.route("/<poi_id>", methods=["GET", "PUT", "DELETE"])
def hotel_instance_manager(poi_id):
    if request.method == "GET":
        poi = poi_dao.get_poi(poi_id)
        if poi:
            return json.dumps(poi.to_dict())
        res = make_response(jsonify({"error": "Point of interest not found."}), 400)
        return res
    elif request.method == "PUT":
        poi = PointOfInterest.dict_to_cls(json.loads(request.json))
        if poi_dao.put_poi(poi, poi_id):
            res = make_response(jsonify({"message": "Point of interest modified"}), 200)
            return res
        res = make_response(jsonify({"message": "Point of interest do not exist"}), 404)
        return res
    elif request.method == "DELETE":
        if poi_dao.delete_poi(poi_id):
            res = make_response(jsonify({"message": "Point of interest deleted"}), 200)
            return res
        res = make_response(jsonify({"message": "Point of interest do not exist"}), 404)
        return res

def _fill_database():
    # poi_dao.delete_pois("") remove all pois
    df_p = pd.read_csv(os.path.join("", "../poi_dataset.csv"), delimiter=",")
    poi_list = PoiList.pandas_to_cls(df_p[df_p["countryName"] == "Switzerland"])
    poi_dao.add_pois(poi_list)

#call only if wants to completely refill the db
#_fill_database()





