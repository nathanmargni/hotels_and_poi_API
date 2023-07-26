import json
from flask import Blueprint, request, redirect, make_response, jsonify
import requests
import os
import pandas as pd

from objects.address import Address
from objects.hotel import Hotel
from objects.hotel_list import HotelList
from db.hotel_dao import HotelDao
from objects.position import Position

hotel = Blueprint('hotel', __name__, url_prefix='/hotels')
hotel_dao = HotelDao()


@hotel.route("/", methods=["GET", "POST"])
def hotel_collection_manager():
    if request.method == "GET":
        args = request.args.to_dict()
        if args.get('sort_by', None) is not None:
            sort_by = args.pop('sort_by')
            direction = -1 if sort_by[0] == '-' else 1
            sort_by = sort_by[1:]
        else:
            sort_by = None
            direction = 0
        #between is the parameter used as filter for the range
        #start and and could be empty and the respective condition will not be set.
        if args.get('between', None) is not None and (args.get('start', None) is not None or args.get('end', None) is not None):
            start = args.pop('start', None)
            end = args.pop( 'end', None )
            return json.dumps( hotel_dao.get_hotels_by_range( parameter=args['between'], start=start, end=end, sort_by=sort_by, direction=direction ).to_json() )
        return json.dumps( hotel_dao.get_hotels(parameters=args, sort_by=sort_by, direction=direction).to_json() )
    elif request.method == "POST":
        hotel = Hotel.dict_to_cls(json.loads(request.json))
        if not hotel_dao.add_hotel(hotel):
            res = make_response( jsonify( {"error": "Hotel already exists"} ), 400)
            return res
        res = make_response( jsonify( {"message": "Hotel created"} ), 201 )
        return res

@hotel.route("/<hotel_id>", methods=["GET", "PUT", "DELETE"])
def hotel_instance_manager(hotel_id):
    if request.method == "GET":
        hotel = hotel_dao.get_hotel( hotel_id )
        if hotel:
            return json.dumps( hotel.to_dict() )
        res = make_response( jsonify( {"error": "Hotel not found."} ), 400 )
        return res
    elif request.method == "PUT":
        hotel = Hotel.dict_to_cls(json.loads(request.json))
        if hotel_dao.put_hotel(hotel, hotel_id):
            res = make_response( jsonify( {"message": "Hotel modified"} ), 200 )
            return res
        res = make_response( jsonify( {"message": "Hotel do not exist"} ), 404 )
        return res
    elif request.method == "DELETE":
        if hotel_dao.delete_hotel( hotel_id):
            res = make_response( jsonify( {"message": "Hotel deleted"} ), 200 )
            return res
        res = make_response( jsonify( {"message": "Hotel do not exist"} ), 404 )
        return res

def _fill_database():
    #hotel_dao.delete_hotels("") remove all hotels
    df_h = pd.read_csv( os.path.join( "", "../hotels_dataset.csv" ), delimiter="," )
    hotel_list = HotelList.pandas_to_cls(df_h[df_h["countryName"] == "Switzerland"])
    hotel_dao.add_hotels(hotel_list)

#call only if wants to completely refill the db
#_fill_database()


