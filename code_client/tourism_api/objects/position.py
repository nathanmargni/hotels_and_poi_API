from math import sin, cos, sqrt, atan2, radians

class Position:
    KEYS = {'latitude': 'latitude', 'longitude': 'longitude'}

    def __init__(self, latitude: float=None, longitude: float=None):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        if latitude is None:
            self.__latitude = None
        else:
            self.__latitude = latitude if latitude >= -90 and latitude <= 90 else None

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        if longitude is None:
            self.__longitude = None
        else:
            self.__longitude = longitude if longitude >= -180 and longitude <= 180 else None

    def to_dict(self):
        return {
            Position.KEYS['longitude']: self.longitude,
            Position.KEYS['latitude']: self.latitude
        }

    def distance_to(self, position2):
        R = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(position2.latitude)
        lon2 = radians(position2.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return  round(R * c * 100,0) # in meters