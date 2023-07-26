from tourism_api.objects.place import Place
from tourism_api.objects.position import Position
from tourism_api.objects.address import Address
import pandas as pd


class PointOfInterest(Place):
    KEYS = {
        'poiId': 'poiId', 'name': 'poiName', 'category': 'category', 'subcategory': 'subcategory',
        'opening_hours': 'openingHours', 'other_tags': 'otherTags', 'address': Address.KEYS, 'position': Position.KEYS
    }

    _PRIMARY_KEY = []

    def __init__(self, id: int, name: str, category: str, subcategory: str, opening_hours: str, other_tags: dict,
                 address: Address, position: Position):
        Place.__init__(self, address, position)
        self.poi_id = id
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.opening_hours = opening_hours
        self.other_tags = other_tags

    def to_dict(self, nested= True):
        output = {PointOfInterest.KEYS['poiId']: self.poi_id, PointOfInterest.KEYS['name']: self.name,
                      PointOfInterest.KEYS['category']: self.category,
                      PointOfInterest.KEYS['subcategory']: self.subcategory,
                      PointOfInterest.KEYS['opening_hours']: self.opening_hours,
                      PointOfInterest.KEYS['other_tags']: self.other_tags}
        if nested:
            output['address'] = self.address.to_dict()
            output['position'] = self.position.to_dict()
        else:
            output.update( Address.to_dict( self.address ) )
            output.update( Position.to_dict( self.position ) )
        return output

    def to_row(self):
        output = {PointOfInterest.KEYS['poiId']: self.poi_id, PointOfInterest.KEYS['category']: self.category,
                  PointOfInterest.KEYS['subcategory']: self.subcategory,
                  PointOfInterest.KEYS['opening_hours']: self.opening_hours,
                  PointOfInterest.KEYS['other_tags']: self.other_tags}
        output.update(Address.to_dict(self.address))
        output.update( Position.to_dict( self.position ) )
        return output


    @classmethod
    def dict_to_cls(cls, poi, nested = True):
        pois_list = []

        # Define if the list is nested stored and which level have to consider
        # for the field search.
        address_level = cls._nested_helper(poi, "address", nested)
        position_level = cls._nested_helper(poi, "position", nested)

        output = PointOfInterest(id=cls._parse_int(poi[PointOfInterest.KEYS['poiId']]), name=poi[PointOfInterest.KEYS['name']],
                            category=str(poi[PointOfInterest.KEYS['category']]),
                            subcategory=str(poi[PointOfInterest.KEYS['subcategory']]),
                            opening_hours=str(poi[PointOfInterest.KEYS['opening_hours']]),
                            other_tags=poi[PointOfInterest.KEYS['other_tags']],
                            address=Address(
                                country=address_level[PointOfInterest.KEYS['address']['countryName']],
                                # code=address_level[Hotel.KEYS['address']['countryCode']],
                                city=address_level[PointOfInterest.KEYS['address']['cityName']],
                                # street=address_level[Hotel.KEYS['address']['street']]
                            ),
                            position=Position(
                                latitude=cls._parse_float(position_level[PointOfInterest.KEYS['position']['latitude']]),
                                longitude=cls._parse_float(position_level[PointOfInterest.KEYS['position']['longitude']]))
                            )
        return output

    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        return int(value)

    @staticmethod
    def _parse_float(value):
        if value is None:
            return None
        return float(value)


    def cls_to_pandas(self):
        output = pd.DataFrame()
        output = output.append( self.to_dict(nested=False), ignore_index=True )
        return output

    @staticmethod
    def _nested_helper(poi, field, nested):
        # poi['address'] is for data stored in nested dictionaries (mongoDB), poi is for plain database such csv.
        return poi[field] if nested else poi
    def __repr__(self) -> str:
        return str(self.to_dict())
