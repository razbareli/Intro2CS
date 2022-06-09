##########################################################
# FILE:wordsearch.py
# WRITER:Raz_Bareli unixraz 203488747
# EXERCISE:intro2cs1 ex5 2021
# DESCRIPTION: looking up words within a matrix of letters
##########################################################

import sys
import os

def read_wordlist(filename):
    """reads a text file and creates a list from the words in it
     :param filename: the text file with the words, each word in a new line
     :return: a list with the words from the text file"""
    f = open(filename, 'r')
    word_list = []
    for line in f:
        word_list.append(line[:-1])
    f.close()
    return word_list

def read_matrix(filename):
    """converts a matrix text file to a list of lists
    :param: the text file with the matrix
    :return: list of list, in which each inner list is a row within the matrix"""
    f = open(filename, 'r')
    matrix = []
    for lines in f:
        lst = []
        line = lines[:-1]
        for letter in line:
            if letter != ",":
                lst.append(letter)
        matrix.append(lst)
    f.close()
    return matrix

#searches for words in a matrix, in a direction from left to right
def find_words_in_matrix(word_list, matrix, words_dictionary):
    """finds words within a horizontal matrix - looks for a word in separate rows.
    :param: word_list: the words we want to search for. matrix: the matrix we want to search in.
    words_dictionary: the count of each word in the matrix that was already found
    :returns: an updated words_dictionary as explained above"""
    for word in word_list:
        for row in range(len(matrix)):
            for letter in range(len(matrix[row])):
                if word[0] == matrix[row][letter] and len(matrix[row][letter:]) >= len(word):
                    if word in "".join(matrix[row][letter:letter+len(word)]):
                        if word in words_dictionary:
                            words_dictionary[word] = words_dictionary[word]+1
                        else:
                            words_dictionary[word] = 1

    return words_dictionary

def reverse_matrix(matrix):
    """inverses each line in a matrix from end to start"""
    reversed_matrix = []
    for row in matrix:
        row = list(reversed(row))
        reversed_matrix.append(row)
    return reversed_matrix

def matrix_l(matrix):
    """prepares the matrix to search right to left"""
    matrix_l = reverse_matrix(matrix)
    return matrix_l

def matrix_d(matrix):
    """prepare matrix to search up to down"""
    matrix_d = []
    for col in range(len(matrix[0])):
        lst = []
        for row in range(len(matrix)):
            lst.append(matrix[row][col])
        matrix_d.append(lst)
    return matrix_d

def matrix_u(matrix):
    """prepare matrix to search down to up"""
    matrix_u = reverse_matrix(matrix_d(matrix))
    return matrix_u

def matrix_z(matrix):
    """prepare matrix to search diagonally down and left"""
    matrix_z = [[] for lst in range(len(matrix[0])+len(matrix)-1)]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            matrix_z[row+col].append(matrix[row][col])
    return matrix_z

def matrix_w(matrix):
    """prepare matrix to search diagonally up and right"""
    matrix_w = reverse_matrix(matrix_z(matrix))
    return matrix_w

def matrix_y(matrix):
    """prepare matrix to search diagonally down and right"""
    matrix_y = [[] for lst in range(len(matrix[0]) + len(matrix) - 1)]
    if len(matrix) <= len(matrix[0]):
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                matrix_y[col-row-len(matrix)+1].append(matrix[row][col])
        return matrix_y
    else:
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                matrix_y[col-row-len(matrix[0])+1].append(matrix[row][col])
        return matrix_y

def matrix_x(matrix):
    """prepare matrix to search diagonally up and left"""
    matrix_x = reverse_matrix(matrix_y(matrix))
    return matrix_x

def find_words(word_list, matrix, directions):
    """finds words in a matrix within the given directions
    :param: word_list: the words we want to search for. matrix: the matrix we want to search in.
    directions: the directions we want to look for the words in the matrix
    :return: list of tuples, each one contains the word and it's counts"""
    directions = set(directions)
    list_of_directions = []
    for letter in directions:
        if letter == 'u':
            list_of_directions.append(matrix_u(matrix))
        if letter == 'd':
            list_of_directions.append(matrix_d(matrix))
        if letter == 'r':
            list_of_directions.append(matrix)
        if letter == 'l':
            list_of_directions.append(matrix_l(matrix))
        if letter == 'w':
            list_of_directions.append(matrix_w(matrix))
        if letter == 'x':
            list_of_directions.append(matrix_x(matrix))
        if letter == 'y':
            list_of_directions.append(matrix_y(matrix))
        if letter == 'z':
            list_of_directions.append(matrix_z(matrix))
    words_dictionary = {}
    for lst in list_of_directions:
        words_dictionary = find_words_in_matrix(word_list, lst, words_dictionary)
        list_words_count = list(words_dictionary.items())
    return list_words_count

def write_output(results, filename):
    list_of_results = [i[0]+','+str(i[1])+'\n' for i in results]
    f = open(filename, 'w')
    f.writelines(list_of_results)
    f.close()

def write_empty_file(filename):
    f = open(filename, 'w')
    f.close()

def check_input(word_file, matrix_file, directions):
    """checks whether the input files are as expected
     :param: the word file, matrix file and searching directions
     :return: False if one of the above does not exist or does not meet the requirements. True else"""
    if not os.path.exists(word_file):
        print ("the word file is missing")
        return False
    elif not os.path.exists(matrix_file):
        print("the matrix file is missing")
        return False
    elif not len(sys.argv) == 5:
        print("the number of parameters are wrong")
        return False
    else:
        for i in directions:
            if i not in 'udlrwxyz':
                print("the directions parameters are wrong")
                return False
        return True

def main():
    """calls all the functions in order, to complete the program"""
    if check_input(sys.argv[1], sys.argv[2], sys.argv[4]) == False:
        sys.exit()
    WORD_LIST = read_wordlist(sys.argv[1])
    MATRIX = read_matrix(sys.argv[2])
    if len(WORD_LIST) == 0 or len(MATRIX) == 0:
        write_empty_file(sys.argv[3])
    else:
        DIRECTIONS = sys.argv[4]
        OUTPUT_FILE = sys.argv[3]
        TUPLES_OF_RESULTS = find_words(WORD_LIST, MATRIX, DIRECTIONS)
        write_output(TUPLES_OF_RESULTS, OUTPUT_FILE)

if __name__ == '__main__':
    main()

