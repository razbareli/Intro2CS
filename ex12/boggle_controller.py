import boggle_gui
import tkinter as tk
import boggle_board_randomizer
import ex12_utils
from tkinter import messagebox


class Boggle_controller:
    # the __init__ method for the Boggle_controller class
    def __init__(self, board, words, gui_obj):
        self.__gui = gui_obj
        self.__board = board
        self.__words_dict = words
        self.__current_word = ''
        self.__words_found = {}
        self.__buttons = self.__gui.get_buttons_dict()
        self.__right_buttons = self.__gui.get_right_buttons()
        self.__check_word_button = self.__right_buttons['check\nword']
        self.__hint_button = self.__right_buttons['hint']

    # A method that runs the Boggle_controller, made for tests.
    def run(self):
        self.gui_controller_match_command()
        self.__gui.run()

    # A method that assigns the check word button it's logic method
    def config_check_button(self):
        self.__check_word_button.config(command=self.button_command_logic)

    # A method that assigns the check word button it's logic method
    def config_hint_button(self):
        self.__hint_button.config(command=self.hint)

    # A method that handles the logic for the check word button.
    def button_command_logic(self):
        word = self.__current_word

        if self.check_if_word(word):
            try:
                if self.__words_found[word]:
                    self.__gui.word_already_found(word)
            except KeyError:
                self.__words_found[word] = True
                self.__gui.add_word_to_words_found(word)
                return self.points_from_word()
            finally:
                self.__current_word = ''

    # A method that checks if a word is in the words dictionary.
    def check_if_word(self, word):
        try:
            if self.__words_dict[word]:
                return True
        except KeyError:
            return False

    # A method that binds the gui_controller_match method to all buttons in the gui
    def gui_controller_match_command(self):
        for button in self.__buttons.keys():
            button.bind('<Motion>', self.gui_controller_match)

    # A method that makes sure the controller is aware of what letters are in the gui screen
    # at all times, and what buttons are pressed and what their locations are
    def gui_controller_match(self, event):
        self.__current_word = self.__gui.get_word_on_screen()

    # A method that calculates how many points a found word should award the player and releases all
    # buttons
    def points_from_word(self):
        score = len(self.__current_word) ** 2
        self.__gui.update_score(score)
        self.__gui.release_all_buttons()

    # A method that gives the player a hint
    def hint(self):
        msg = messagebox.askquestion(title='HINT', message='You will pay 10 points, and if you are one letter close - the hint will tell you the missing letter!!\nProceed?')
        if msg != 'yes':
            return
        letters = self.__current_word
        if len(letters) < 2 or len(letters) > 6:
            messagebox.showinfo(title='HINT', message="You can use a hint after choosing a minimum of 2 letter and up to 6 letters")
            return
        self.__gui.update_score(-10)
        if letters in self.__words_dict:
            messagebox.showinfo(title='HINT', message="Check the current word, it might exist!")
            return
        words = ex12_utils.find_length_n_words(len(letters) + 1, self.__board, self.__words_dict)
        for i in words:
            if letters == i[0][:len(letters)]:
                messagebox.showinfo(title='HINT', message="You are very close, "+str(i[0][len(letters)])+" is the missing letter!\nNOTE: You may not be on the right path!")
                return
        messagebox.showinfo(title='HINT', message="No way from here... Try something else")
        return


if __name__ == '__main__':
    words_dict = ex12_utils.load_words_dict('boggle_dict.txt')
    game_board = boggle_board_randomizer.randomize_board(boggle_board_randomizer.LETTERS)
    gui = boggle_gui.Board_gui(181, 4, game_board)
    cont = Boggle_controller(game_board, words_dict, gui)
    cont.run()
