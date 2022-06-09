import random


class Ship:

    def __init__(self):
        self.__speed_x = 0
        self.__speed_y = 0
        self.__location_x = random.randint(-500, 500)
        self.__location_y = random.randint(-500, 500)
        self.__direction = 0
        self.__radius = 1
        self.__life = 3

    def get_life(self):
        return self.__life

    def remove_life(self):
        self.__life -= 1

    def get_location_x(self):
        return self.__location_x

    def get_location_y(self):
        return self.__location_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def get_direction(self):
        return self.__direction

    def set_location_x(self, location):
        self.__location_x = location

    def set_location_y(self, location):
        self.__location_y = location

    def set_speed_x(self, speed):
        self.__speed_x = speed

    def set_speed_y(self, speed):
        self.__speed_y = speed

    def set_direction(self, direction):
        self.__direction = direction

    def get_radius(self):
        return self.__radius