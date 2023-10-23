# 3 kyu
"""
DESCRIPTION:
Consider a "word" as any sequence of capital letters A-Z (not limited to 
just "dictionary words"). For any word with at least two different letters, 
there are other words composed of the same letters but in a different order
(for instance, STATIONARILY/ANTIROYALIST, which happen to both be dictionary 
words; for our purposes "AAIILNORSTTY" is also a "word" composed of the 
same letters as these two).

We can then assign a number to every word, based on where it falls in an 
alphabetically sorted list of all words made up of the same group of 
letters. One way to do this would be to generate the entire list of words 
and find the desired one, but this would be slow if the word is long.

Write a function, called "list_position", such that, given a word, it returns 
its number. Your function should be able to accept any word 25 letters or less 
in length (possibly with some letters repeated), and take no more than 500 
milliseconds to run. To compare, when the solution code runs the 27 test cases 
in JS, it takes 101ms.

For very large words, you'll run into number precision issues in JS (if 
the word's position is greater than 2^53). For the JS tests with large 
positions, there's some leeway (.000000001%). If you feel like you're 
getting it right for the smaller ranks, and only failing by rounding on 
the larger, submit a couple more times and see if it takes.

Python, Java and Haskell have arbitrary integer precision, so you must be 
precise in those languages (unless someone corrects me).

C# is using a long, which may not have the best precision, but the tests 
are locked so we can't change it.

Sample words, with their rank:
ABAB = 2
AAAB = 1
BAAA = 4
QUESTION = 24572
BOOKKEEPER = 10743
"""

from math import factorial


def multinomial_coefficient(values):
    numerator = factorial(sum(values))
    denominator = 1
    for value in values:
        denominator *= factorial(value)
    return numerator // denominator


def get_letters_and_multiplicity(word, letters=None, multiplicity=None):
    if letters == None:
        letters = list(set(list(word)))
        letters.sort()
        multiplicity = [0]*len(letters)
    if word == '':
        return letters, multiplicity
    for index in range(len(letters)):
        if word[0] == letters[index]:
            multiplicity[index] += 1
            return get_letters_and_multiplicity(word[1:], letters, multiplicity)


def get_alphabetical_index(letter, lista):
    for k in range(len(lista)):
        if lista[k] == letter:
            return k


def list_position(word, letters=None, multiplicity=None, coefficient=None):
    if letters == None:
        letters, multiplicity = get_letters_and_multiplicity(word)
        coefficient = multinomial_coefficient(multiplicity)
    if len(word) == 1:
        return 1
    k = get_alphabetical_index(word[0], letters)
    new_term = coefficient*sum(multiplicity[:k])//sum(multiplicity)
    coefficient = coefficient*multiplicity[k]//sum(multiplicity)
    if multiplicity[k] == 1:
        del letters[k]
        del multiplicity[k]
    else:
        multiplicity[k] -= 1
    return new_term + list_position(word[1:], letters, multiplicity, coefficient)


keep_going = True
while keep_going:
    print('Please enter a word. Enter "q" to quit.')
    print('-'*60)
    user_input = input()
    if user_input == 'q':
        keep_going = False
    else:
        print(f'{user_input}: \t {list_position(user_input)}')
