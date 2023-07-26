import json

from mongo import Collection

from db.mongo_db import MongoDb
from objects.point_of_interest import PointOfInterest
from objects.poi_list import PoiList


class PoiDao:

    def __init__(self):
        db = MongoDb().db
        self.__pois: Collection = db['poi']

    def add_poi(self, poi: PointOfInterest):

        if self.it_exists(poi.poi_id):
            print("400 db")
            return False
        data = poi.to_dict()
        self.__pois.insert_one(data)
        return data

    def put_poi(self, poi: PointOfInterest, id: int):
        data = poi.to_dict()
        if self.it_exists(id):
            print("update:", data)
            filter = {'poiId': PoiDao._parse_int(id)}
            newvalues = {"$set": data}  # dict, need to be tested
            self.__pois.update_one(filter, newvalues)
            print(self.get_poi(id))
            return data
        print("Poi Not Found")
        return False

    def get_poi(self, poi_id: int):
        print("id searching: ", poi_id)
        poi = self.__pois.find_one({"poiId": PoiDao._parse_int(poi_id)})
        if poi is not None:
            return PointOfInterest.dict_to_cls(poi)
        return False

    def delete_poi(self, id: int):
        if self.it_exists(id):
            self.__pois.delete_one({"poiId": PoiDao._parse_int(id)})
            return True
        return False

    def it_exists(self, poi_id: int):
        return self.__pois.find_one({"poiId": PoiDao._parse_int(poi_id)})

    def add_pois(self, pois):
        for p in pois.values:
            self.add_poi(p)

    #unused by client.
    def delete_pois(self, condition):
        self.__pois.delete_many({condition})

    def get_pois(self, parameters : dict, sort_by :str=None, direction :int=1):
        if sort_by is None:
            return PoiList.dicts_to_cls( list( self.__pois.find( parameters )))

        return PoiList.dicts_to_cls(list(self.__pois.find(parameters).sort(sort_by, direction)))

    def get_pois_by_range(self, parameter : str, start : float=None, end : float=None, sort_by :str=None, direction :int=1):
        rng_filter = {}
        if start is not None:
            rng_filter.update({'$gte': float(start)})
        if end is not None:
            rng_filter.update({'$lte': float(end)})
        if sort_by is None:

            return PoiList.dicts_to_cls(
                list( self.__pois.find( {parameter: rng_filter} ) ) )
        return PoiList.dicts_to_cls( list( self.__pois.find({parameter:rng_filter}).sort(sort_by, direction)))


    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        return int(value)









