"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item not in result:
            result.append(item)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item in list2:
            result.append(item)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    l_1 = list1[:]
    l_2 = list2[:]
    res = []
    while l_1 != [] and l_2 != []:
        list_10 = l_1[0]
        list_20 = l_2[0]
        if list_10 < list_20:
            res.append(list_10)
            l_1.pop(0)
        else:
            res.append(list_20)
            l_2.pop(0)
    res.extend(l_1)
    res.extend(l_2)
    return res
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid_point = len(list1) / 2
    l_1 = list1[0:mid_point]
    l_2 = list1[mid_point:]
    l_1 = merge_sort(l_1)
    l_2 = merge_sort(l_2)
    new_list = merge(l_1, l_2)
    return new_list

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    head = word[0]
    tail = word[1:]
    rest_strings = gen_all_strings(tail)
    new_strings = []
    for string in rest_strings:
        if len(string) == 0:
            new_strings.append(head)
            continue
        length = len(string)
        new_list = [string[:idx] + head + string[idx:] for idx in range(length + 1)]
        new_strings.extend(new_list)
    rest_strings.extend(new_strings)
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    a_file = urllib2.urlopen(codeskulptor.file2url(filename))
    return list(a_file.readlines())

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

print remove_duplicates([1, 3, 3, 8])
print intersect([1, 2, 3, 4], [3, 4, 5, 6])
print merge_sort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
print merge([1, 2, 3], [4, 5, 6])
print gen_all_strings("aab")
