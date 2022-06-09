
class Car:
    """
    creates a car object that can differ in location, name, orientation and length
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        lst = [self.location[:]]
        for i in range(1, self.length):
            if self.orientation == 0:
                lst.append((lst[0][0]+i, lst[0][1]))
            if self.orientation == 1:
                lst.append((lst[0][0], lst[0][1]+i))
        return lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        #For this car type, keys are from 'udrl'
        #The keys for vertical cars are 'u' and 'd'.
        #The keys for horizontal cars are 'l' and 'r'.
        #You may choose appropriate strings.
        # implement your code and erase the "pass"
        #The dictionary returned should look something like this:
        #result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        #A car returning this dictionary supports the commands 'f','d','a'.
        temp = dict()
        if self.orientation == 0:
            temp['u'] = "move up"
            temp['d'] = "move down"
        if self.orientation == 1:
            temp['r'] = "move right"
            temp['l'] = "move left"
        return temp


    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        #For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        #be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        if movekey == 'u':
            return [(self.location[0]-1, self.location[1])]
        elif movekey == 'l':
            return [(self.location[0], self.location[1]-1)]
        elif movekey == 'd':
            return [(self.location[0]+self.length, self.location[1])]
        elif movekey == 'r':
            return [(self.location[0], self.location[1]+self.length)]


    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False
        else:
            if movekey == 'u':
                self.location = (self.location[0]-1, self.location[1])
                return True
            elif movekey == 'l':
                self.location = (self.location[0], self.location[1]-1)
                return True
            elif movekey == 'd':
                self.location = (self.location[0]+1, self.location[1])
                return True
            elif movekey == 'r':
                self.location = (self.location[0], self.location[1]+1)
                return True
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        temp = self.name[:]
        return temp
