##########################################################
# FILE:ex7.py
# WRITER:Raz_Bareli unixraz 203488747
# EXERCISE:intro2cs1 ex7 2021
# DESCRIPTION: recursion functions
##########################################################
from typing import *

#1 prints all integers from 1 to n
def print_to_n(n: int) -> None:
    if n < 1:
        return
    print_to_n(n-1)
    print(n)

#2 calculates the sum of the integers
def digit_sum(n: int) -> int:
    if n == 0:
        return 0
    return digit_sum(n//10) + (n % 10)

#3 determines if a number is prime
def is_prime_helper(n: int, i: int) -> bool:
    if n < 2:
        return False
    if i == n:
        return True
    if n % i == 0:
        return False
    return is_prime_helper(n, i+1)

def is_prime(n: int) -> bool:
    return is_prime_helper(n, 2)

#4 solves the Hanoy puzzle
def play_hanoi(hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> Any:
    if n == 1:
        return hanoi.move(src, dst)
    if n <= 0:
        return
    else:
        play_hanoi(hanoi, n-1, src, temp, dst)
        play_hanoi(hanoi, 1, src, dst, temp)
        play_hanoi(hanoi, n-1, temp, dst, src)

#5 prints all possible sequences, with repetitions of a letter in the sequence
def print_sequences_helper(char_list: List[str], n: int, length: int, letter: str ) -> None:
    if n == 0:
        print(letter)
        return
    for i in range(length):
        next_letter: str = letter + char_list[i]
        print_sequences_helper(char_list, n-1, length, next_letter)

def print_sequences(char_list: List[str], n: int) -> None:
    length = len(char_list)
    print_sequences_helper(char_list, n, length, '')

#6 prints all possible sequences, without repetitions of a letter in the sequence
def print_no_repetition_sequences_helper(char_list: List[str], n: int, length: int, letter: str) -> None:
    if n == 0:
        print(letter)
        return
    for i in range(length):
        if char_list[i] not in letter:
            next_letter: str = letter + char_list[i]
            print_no_repetition_sequences_helper(char_list, n - 1, length, next_letter)

def print_no_repetition_sequences(char_list: List[str], n: int) -> None:
    length: int = len(char_list)
    print_no_repetition_sequences_helper(char_list, n, length, '')

#7 returns a list of the possible legal parentheses sequences
def parentheses_helper(n: int, temp_str: str, lst: List[str]) -> List[str]:
    if len(temp_str) == 2*n:
        count_left: int = 0
        count_right: int = 0
        for i in temp_str:
            if i == "(":
                count_left += 1
            if i == ")" and count_left > count_right:
                count_right += 1
        if count_left == n and count_right == n:
            lst.append(temp_str)
        return lst
    parentheses_helper(n, temp_str + '(', lst)
    parentheses_helper(n, temp_str + ')', lst)
    return lst

def parentheses(n: int) -> List[str]:
    return parentheses_helper(n, '', [])

#8 runs the flood fill algorithm
def flood_fill(image: List[List[str]], start: Tuple[int, int]) -> None:
    flood_fill_helper(image, start)

def flood_fill_helper(image: List[List[str]], start: Tuple[int, int]) -> None:
    if image[start[0]][start[1]] == '*':
        return
    else:
        image[start[0]][start[1]] = '*'
        flood_fill_helper(image, (start[0]-1, start[1]))
        flood_fill_helper(image, (start[0]+1, start[1]))
        flood_fill_helper(image, (start[0], start[1]-1))
        flood_fill_helper(image, (start[0], start[1]+1))
        return
