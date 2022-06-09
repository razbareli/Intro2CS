from math import sqrt


class Asteroid:
    def __init__(self, location_speed_x, location_speed_y, size):
        self.__location_x = location_speed_x[0]
        self.__speed_x = location_speed_x[1]
        self.__location_y = location_speed_y[0]
        self.__speed_y = location_speed_y[1]
        self.__size = size
        self.__radius = self.__size*10 - 5

    def get_radius(self):
        return self.__radius

    def get_location_x(self):
        return self.__location_x

    def get_speed_x(self):
        return self.__speed_x

    def get_location_y(self):
        return self.__location_y

    def get_speed_y(self):
        return self.__speed_y

    def get_size(self):
        return self.__size

    def set_location_x(self, x):
        self.__location_x = x

    def set_location_y(self, y):
        self.__location_y = y

    def get_distance_from_obj(self, game_obj):
        distance = sqrt((game_obj.get_location_x() - self.__location_x) ** 2
                        + (game_obj.get_location_y() - self.__location_y) ** 2)
        return distance

    def has_intersection(self, game_obj):
        """decides if there is an intersection with another object
        :returns True if there is an intersection, False otherwise"""
        distance = self.get_distance_from_obj(game_obj)
        if distance <= self.__radius + game_obj.get_radius():
            return True
        else:
            return False
