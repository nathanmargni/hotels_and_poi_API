from abc import ABC
from tourism_api.objects.address import Address
from tourism_api.objects.position import Position


class Place(ABC):

    def __init__(self, address:Address, position:Position):
        self.position = position
        self.address = address

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value