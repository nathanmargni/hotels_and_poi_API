import json

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import gmplot

from tourism_api.objects.point_of_interest import PointOfInterest
from tourism_api.objects.poi_list import PoiList


class PoiManager:

    def __init__(self):
        pass

    @staticmethod
    def get_pois(params=None, sort_by=None, direction=1):
        if params is None:
            params = {}
        if sort_by is not None:
            params['sort_by'] = ('-' if direction == -1 else "+") + sort_by
        url = 'http://127.0.0.1:5000/pois/'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.get( url, params=params)
        return PoiList.dicts_to_cls(response.json())

    @classmethod
    def get_pois_sorted(cls, sort_by=None, direction=1, params=None):
        if params is None:
            params = {}
        params['sort_by'] = ('-' if direction == -1 else "+") + sort_by
        return cls.get_pois(params)

    @classmethod
    def get_pois_by_country(cls,country : str, sort_by=None, direction=1):
        return cls.get_pois({'address.countryName':country}, sort_by, direction)

    @classmethod
    def get_pois_by_category(cls,category : str, sort_by=None, direction=1):
        return cls.get_pois({'category':category}, sort_by, direction)

    @classmethod
    def get_pois_by_subcategory(cls,subcategory : str, sort_by=None, direction=1):
        return cls.get_pois({'subcategory':subcategory}, sort_by, direction)

    @classmethod
    def get_pois_by_city(cls, city : str, sort_by=None, direction=1):
        return cls.get_pois({'address.cityNAAame':city}, sort_by, direction)

    @classmethod
    def get_poi_by_name(cls, name: str, sort_by=None, direction=1):
        return cls.get_pois({'poiName':name}, sort_by, direction)


    @staticmethod
    def add_poi(poi : PointOfInterest):
        url = f'http://127.0.0.1:5000/pois/'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.post( url, json=json.dumps( poi.to_dict() ), timeout=5 )
        return response.text

    @staticmethod
    def update_poi(poi : PointOfInterest):
        url = f'http://127.0.0.1:5000/pois/{poi.poi_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.put( url, json=json.dumps( poi.to_dict() ), timeout=5 )
        return response.text


    @staticmethod
    def get_poi_by_id(poi_id : int):
        url = f'http://127.0.0.1:5000/pois/{poi_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.get( url )
        if "error" in response.json().keys():
            return response.json()["error"]
        else:
            return PointOfInterest.dict_to_cls(response.json())


    @staticmethod
    def delete_poi_by_id(poi_id : int):
        url = f'http://127.0.0.1:5000/pois/{poi_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.delete( url, timeout=5 )
        return response.text


    @staticmethod
    def save_map(poilist: PoiList, filename: str = None, get_string=False):

        df = poilist.cls_to_pandas()
        lat = 46.8
        lon = 8.3

        apikey = "AIzaSyDyj9f9lYTrfwqrs0vdMNtmgCU2cnH9h4Y"
        map_styles = [{"featureType": "poi", "stylers": [{"Visibility": "off"}]}]
        gmap = gmplot.GoogleMapPlotter(lat, lon, 8, radius=40, scale_control=False, apikey=apikey, title="Pois")

        for i, row in df.iterrows():
            gmap.marker(row['latitude'], row['longitude'], title=row["subcategory"], info_window=" category: " +
                                                        str(row["category"]) + ", " + str(row["subcategory"]))

        if filename is None or get_string is True:
            return gmap.get()
        else:
            gmap.draw(filename)

