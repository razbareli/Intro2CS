######################################
# FILE:ex4.py
# WRITER:Raz_Bareli unixraz 203488747
# EXERCISE:intro2cs1 ex4 2021
# DESCRIPTION: Hangman Game
######################################

from hangman_helper import *

def update_word_pattern(word, pattern, letter):
    """returns the updated guessed pattern"""
    pattern = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            pattern[i] = word[i]
    return "".join(pattern)

def run_single_game(words_list, score):
    """runs a single game of hangman and returns the score"""
    word = get_random_word(words_list)
    mistakes = []
    pattern = '_' * len(word)
    message = "lets start playing hangman!"
    while pattern != word and score > 0:
        display_state(pattern, mistakes, score, message)
        guess = get_input()

        #if the player asks for a hint
        if guess[0] == HINT:
            score -= 1
            hints = filter_words_list(words_list, pattern, mistakes)
            if len(hints) <= HINT_LENGTH:
                show_suggestions(hints)
            else:
                hints_short = []
                for i in range(HINT_LENGTH):
                    hints_short.append(hints[i*len(hints)//HINT_LENGTH])
                show_suggestions(hints_short)

        #if the player guesses a letter            
        if guess[0] == LETTER:
            #this section checkes that the input is valid
            if len(guess[1]) != 1 or guess[1].isupper() or not guess[1].isalpha():
                message = "please pick a singe lowercase letter"
                continue
            elif guess[1] in mistakes or guess[1] in pattern:
                message = "please guess a letter that was not guessed before"
                continue
            #this section checkes if the word is a orrect guess
            else:
                score -= 1
                if guess[1] in word:
                    pattern = update_word_pattern(word, pattern, guess[1])
                    n = 0
                    for i in word:
                        if guess[1] == i:
                            n += 1
                    score += (n * (n+1) // 2)
                    message = "good job, you've guessed a letter"
                else:
                    mistakes.append(guess[1])
                    message = "this letter is not in the word"

        #if the player guesses a word
        if guess[0] == WORD:
            score -= 1
            if guess[1] == word:
                n = 0
                for i in pattern:
                    if i == "_":
                        n += 1
                score += (n * (n+1) // 2)
                message = "youv'e guessed the correct word!"                
                display_state(pattern, mistakes, score, message)
                return score
            else:
                message = "the word you've guessed is wrong"
                continue

    #determines if the player won or lost
    if pattern == word:
        message = "you WON the game"
        display_state(pattern, mistakes, score, message)
    else:
        message = "you LOST the game, the word was " + word
        display_state(pattern, mistakes, score, message)
    return score


def filter_words_list(words, pattern, wrong_guess_lst):
    """filter out words that are not eligble for a hint"""
    hints = []
    for i in words:
        if len(i) == len(pattern):
            letter_in_both = True
            for a, j in zip(i, pattern):
                if j.isalpha():
                    if j != a or i.count(a) != pattern.count(a):
                        letter_in_both = False
            if letter_in_both:
                add_to_hints = True
                for k in wrong_guess_lst:
                    if k in i:
                        add_to_hints = False
                if add_to_hints:
                    hints.append(i)
    return hints

def main():
    """runs the entire program, until the player chosses not to play anymore"""
    num_of_games = 0
    words = load_words()
    score = run_single_game(words, POINTS_INITIAL)
    num_of_games += 1
    while score > 0:
        if play_again("you have played " + str(num_of_games) + " games, your score is " + str(score) + " points, should we play again?"):
            score = run_single_game(words, score)
            num_of_games += 1
        else:
            return
    if play_again("you have played " + str(num_of_games) + " games, but now you have no points, restart the game?"):
        main()

if __name__ == "__main__":
    main()

