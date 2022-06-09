from screen import Screen
from asteroid import Asteroid
from ship import Ship
from torpedo import Torpedo
import sys
from math import sin, cos, radians, sqrt
from random import randint

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__asteroids = {}
        self.__torpedos = {}
        self.__total_torps_fired = 0
        self.__ship = Ship()
        self.__points = 0
        self.__torpedo_life_span = 200
        self.__max_torpedos = 10
        self.__asteroids_amount = asteroids_amount
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def add_asteroids(self):
        """adds the asteroids to the game, according to the default asteroids amount"""
        for ast in range(1, self.__asteroids_amount + 1):
            ast_name = f'asteroid_{ast}'
            ast_x = randint(self.__screen_min_x, self.__screen_max_x)
            ast_y = randint(self.__screen_min_y, self.__screen_max_y)
            ast_size = 3
            ast_speed_x = randint(-4, 4)
            if ast_speed_x == 0:
                ast_speed_x = 1
            ast_speed_y = randint(-4, 4)
            if ast_speed_y == 0:
                ast_speed_y = 1
            vars()[ast_name] = Asteroid([ast_x, ast_speed_x], [ast_y, ast_speed_y], ast_size)
            self.__asteroids[ast_name] = vars()[ast_name]
            self.__screen.register_asteroid(vars()[ast_name], ast_size)

    def move_object(self, game_objet):
        """calculates the new location of an object
        :param a game object that can be moved
        :return the new location of the object"""
        new_location_x = self.__screen_min_x + \
                         (game_objet.get_location_x() + game_objet.get_speed_x() - self.__screen_min_x) \
                         % (self.__screen_max_x - self.__screen_min_x)
        new_location_y = self.__screen_min_y + \
                         (game_objet.get_location_y() + game_objet.get_speed_y() - self.__screen_min_y) \
                         % (self.__screen_max_y - self.__screen_min_y)
        game_objet.set_location_x(new_location_x)
        game_objet.set_location_y(new_location_y)
        return

    def turn_ship(self):
        """changes the ship's direction according to the arrow being pressed"""
        if self.__screen.is_left_pressed():
            left = self.__ship.get_direction() + 7
            self.__ship.set_direction(left)
        if self.__screen.is_right_pressed():
            right = self.__ship.get_direction() - 7
            self.__ship.set_direction(right)

    def accelerate(self):
        """changes the speed of the ship when the "up" arrow is pressed"""
        if self.__screen.is_up_pressed():
            new_speed_x = self.__ship.get_speed_x() + cos(radians(self.__ship.get_direction()))
            new_speed_y = self.__ship.get_speed_y() + sin(radians(self.__ship.get_direction()))
            self.__ship.set_speed_x(new_speed_x)
            self.__ship.set_speed_y(new_speed_y)

    def ast_handling(self):
        """handles the asteroid object during the game.
        this function draws, moves, and removes an asteroid from the game.
         It also reduces the ship's life then it collides with an asteroid"""
        for ast_name, ast in self.__asteroids.items():
            self.__screen.draw_asteroid(ast, ast.get_location_x(), ast.get_location_y())
            self.move_object(ast)
            has_collided = ast.has_intersection(self.__ship)
            if has_collided:
                if self.__ship.get_life() == 3:
                    self.__screen.show_message('Collision detected', 'She can take it captain! carry on!')
                elif self.__ship.get_life() == 2:
                    self.__screen.show_message('Collision detected', 'The shields are down captain!\n'
                                                                     'One more hit and we are done for!')
                self.__ship.remove_life()
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(ast)
                self.__asteroids.pop(ast_name)
                break

    def check_for_torpedo_fire(self):
        """adds a torpedo object to the game, if the space-bar is pressed during the game"""
        if self.__screen.is_space_pressed():
            if len(self.__torpedos) >= self.__max_torpedos:
                return
            torpedo_location_x = self.__ship.get_location_x()
            torpedo_location_y = self.__ship.get_location_y()
            torpedo_speed_x = (self.__ship.get_speed_x() + 2 * (cos(radians(self.__ship.get_direction()))))
            torpedo_speed_y = (self.__ship.get_speed_y() + 2 * (sin(radians(self.__ship.get_direction()))))
            torpedo_direction = self.__ship.get_direction()
            self.__total_torps_fired += 1
            torpedo_name = f'torpedo_{self.__total_torps_fired}'
            vars()[torpedo_name] = Torpedo(torpedo_location_x, torpedo_location_y,
                                           torpedo_speed_y, torpedo_speed_x, torpedo_direction)
            self.__torpedos[torpedo_name] = vars()[torpedo_name]
            self.__screen.register_torpedo(vars()[torpedo_name])

    def torpedo_handling(self):
        """handles the torpedo object during the game.
        this function draws, moves and removes torpedo object during the game.
        it also handles the collision between a torpedo and asteroid object"""
        torpedos_to_remove = []
        asteroids_to_add = []
        asteroids_to_remove = []
        for torp_name, torp in self.__torpedos.items():
            self.__screen.draw_torpedo(torp, torp.get_location_x(), torp.get_location_y(), torp.get_direction())
            self.move_object(torp)
            torp.add_to_life_span()
        for torp_name, torp in self.__torpedos.items():
            if torp.get_life_span() >= self.__torpedo_life_span:
                self.__screen.unregister_torpedo(torp)
                self.__torpedos.pop(torp_name)
                break
            for ast_name, ast in self.__asteroids.items():
                has_collided = ast.has_intersection(torp)
                if has_collided:
                    if ast.get_size() == 3:
                        self.__points += 20
                    elif ast.get_size() == 2:
                        self.__points += 50
                    else:
                        self.__points += 100
                    if ast.get_size() > 1:
                        new_asteroid_1_speed_x = ((torp.get_speed_x() + ast.get_speed_x()) /
                                                  sqrt(ast.get_speed_x() ** 2 + ast.get_speed_y() ** 2))
                        new_asteroid_2_speed_x = -((torp.get_speed_x() + ast.get_speed_x()) /
                                                   sqrt(ast.get_speed_x() ** 2 + ast.get_speed_y() ** 2))
                        new_asteroid_1_speed_y = ((torp.get_speed_y() + ast.get_speed_y()) /
                                                  sqrt(ast.get_speed_x() ** 2 + ast.get_speed_y() ** 2))
                        new_asteroid_2_speed_y = -((torp.get_speed_y() + ast.get_speed_y()) /
                                                   sqrt(ast.get_speed_x() ** 2 + ast.get_speed_y() ** 2))
                        asteroid_name_1 = f'asteroid_{ast_name}_1'
                        asteroid_name_2 = f'asteroid_{ast_name}_2'
                        vars()[asteroid_name_1] = Asteroid([ast.get_location_x(), new_asteroid_1_speed_x],
                                                           [ast.get_location_y(), new_asteroid_1_speed_y],
                                                           ast.get_size() - 1)
                        self.__screen.register_asteroid(vars()[asteroid_name_1], ast.get_size() - 1)
                        vars()[asteroid_name_2] = Asteroid([ast.get_location_x(), new_asteroid_2_speed_x],
                                                           [ast.get_location_y(), new_asteroid_2_speed_y],
                                                           ast.get_size() - 1)
                        self.__screen.register_asteroid(vars()[asteroid_name_2], ast.get_size() - 1)
                        asteroids_to_add.append(asteroid_name_1)
                        asteroids_to_add.append(asteroid_name_2)
                    asteroids_to_remove.append(ast_name)
                    torpedos_to_remove.append(torp_name)
                    self.__screen.unregister_torpedo(torp)
                    self.__screen.set_score(self.__points)
                    self.__screen.unregister_asteroid(ast)
        for ast_new in asteroids_to_add:
            self.__asteroids[ast_new] = vars()[ast_new]
        for ast_dead in asteroids_to_remove:
            self.__asteroids.pop(ast_dead)
        for torp_dead in torpedos_to_remove:
            self.__torpedos.pop(torp_dead)

    def _game_loop(self):
        self.move_object(self.__ship)
        self.turn_ship()
        self.accelerate()
        self.__screen.draw_ship(self.__ship.get_location_x(), self.__ship.get_location_y(),
                                self.__ship.get_direction())
        self.ast_handling()
        self.check_for_torpedo_fire()
        self.torpedo_handling()
        if self.__ship.get_life() == 0:
            self.__screen.show_message('You lost!', 'You have run out of life, better luck next time!')
            self.__screen.end_game()
            sys.exit()
        elif len(self.__asteroids) == 0:
            self.__screen.show_message('Victory!', f'You have won the game! congrats!\n '
                                                   f'You have earned {self.__points} points!')
            self.__screen.end_game()
            sys.exit()
        elif self.__screen.should_end():
            self.__screen.show_message('Exit Game', 'You have exited the game.')
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.add_asteroids()
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
