#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4

@author: Michael
"""

import requests
import json

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    API_KEY = config_data['API_KEY']
    STOP_WORDS = set(config_data['STOP_WORDS'])
    
"""For efficiency, STOP_WORDS includes formatting strings to prevent multiple loops.
Each entry is a list with the first member of the list being the unmeaningful term, and the
second member being the character(s) to replace the term with.
"""

# The below strings do not follow PEP-8 guidelines due to it causing
# formatting errors in the command line interface.
WELCOME_MESSAGE = "Welcome to the Etsy Top Terms Identifier. Press Enter to begin."
USER_PROMPT = "Enter the name of an Etsy store you want analysed. Type 'exit' to quit the program: "
CONNECTION_ERROR_MESSAGE = "It looks like you don't have internet. Please connect to the internet and press enter to try again."
CANNOT_FIND_SHOP_ERROR_MESSAGE = "Sorry! We can't find "
RUNNING_ANALYSIS_MESSAGE = "Running Analysis... Depending on your internet connection, this may take a moment."


def get_shop_listings(shop_name):
    """
    Gets the listings for the Etsy shop by name.

    Parameters
    ----------
    shop_name : STRING
        The name of the Etsy shop, as it appears in the site url.

    Returns
    -------
    shop_listings : LIST OF DICTIONARIES or BOOLEAN
        The listings returned by Etsy's api. This is returned None if the shop
        was not found.

    """
    url = f"https://openapi.etsy.com/v2/shops/:shop_id/listings/active?api_key={API_KEY}"
    parameters = {'shop_id': shop_name}
    shop = requests.get(url, params=parameters)
    if shop.status_code == 200:
        shop_listings = json.loads(shop.text)['results']
    else:
        shop_listings = None

    return shop_listings

def remove_non_alpha(word):
    """
    Removes all non-alpha characters from a single word.

    Parameters
    ----------
    word : STRING
        A single word to be processed

    Returns
    -------
    word : STRING
        The input word with all non-alpha characters removed

    """
    word = [character for character in word if character.isalpha()]
    word = ''.join(word)
    return word


def clean_words(words, shop_name):
    """
    Removes all non-alpha characters and stop words from all words in the
    provided list.

    Parameters
    ----------
    words : LIST OF STRINGS
        A list of single words to be cleaned.
    shop_name : STRING
        The name of the shop these words come from.

    Returns
    -------
    new_words : LIST OF STRINGS
        All words that were not stop words and contained alpha-characters,
        with all non-alpha characters removed.

    """
    new_words = []
    # Remove non-alpha characters
    for n, word in enumerate(words):
        if not word.isalpha() and word != shop_name:
            word = remove_non_alpha(word)
            if word != '':
                new_words.append(word)
        else:
            new_words.append(word)

        words[n] = word

    # Remove unmeaningful words
    new_words = [word for word in new_words if word not in STOP_WORDS]
    return new_words


def get_descriptions_and_titles(shop_listings):
    """
    Gets the words that make up the descriptions and titles of the shop's
    listings.

    Parameters
    ----------
    shop_listings : LIST OF DICTIONARIES
        All of the listings for a single Etsy shop.

    Returns
    -------
    shop_words : LIST OF STRINGS
        All of the words from the titles and descriptions of the shop listings.

    """
    shop_words = []
    for listing in shop_listings:

        # API returns listings for unavailable items that have no description
        # or title. The try-except logic below handles those unavailable
        # listings.

        try:
            shop_words += listing['description'].upper().split()
        except KeyError:
            pass
        try:
            shop_words += listing['title'].upper().split()
        except KeyError:
            pass

    return shop_words


def get_shops_and_listings(shop_names):
    """
    Gets the top 5 words for each shop provided.

    Parameters
    ----------
    shop_names : LIST OF STRINGS
        The names of each shop to be analyzed as they appear in their Etsy url.

    Returns
    -------
    shops : LIST OF LISTS
        Each entry is a list pair of the shop_name and the list of the top 5
        words for that shop with their word-count. If the shop was not found,
        then index 1 of each list pair is None.

    """
    shops = []

    for shop_name in shop_names:
        shop_listings = get_shop_listings(shop_name)
        if shop_listings:
            shop_words = get_descriptions_and_titles(shop_listings)
            shop_words = clean_words(shop_words, shop_name)
            top_5_words = get_top_n_counts(shop_words, 5)
            shops.append([shop_name, top_5_words])
        else:
            shops.append([shop_name, None])

    return shops


def get_unique_terms_counts(words):
    """
    Gets the number of times each word appears in a set of words.

    Parameters
    ----------
    words : LIST OF WORDS
        The words to be analyzed.

    Returns
    -------
    word_counts : DICTIONARY
        The keys for the dictionary are the unique words from the provided
        words, with the value being the number of times that word appeared in
        the provided set of words.

    """
    unique_words = set(words)
    word_counts = {}
    for word in unique_words:
        count = words.count(word)
        word_counts[word] = count

    return word_counts


def get_top_n_counts(words, n):
    """
    Get the n number of top words for each word provided.

    Parameters
    ----------
    words : LIST OF STRINGS
        The list of words to be analyzed.
    n : INTEGER
        The number of top words to be identified in the analysis.

    Returns
    -------
    top_words : LIST OF LISTS
        Each entry is a list pair of a word and its word count. This list is
        ordered from most-often appearing word to least-often appearing word.

    """
    top_words = []
    word_counts = get_unique_terms_counts(words)
    for _ in range(n):
        top_word = max(word_counts, key=lambda key: word_counts[key])
        top_words.append([top_word, word_counts[top_word]])
        del word_counts[top_word]

    return top_words


def format_analysis_for_console(shop):
    
    words_string = ""
    for word_count in shop[1]:
        words_string += f"{word_count}"
        
    return words_string

def print_shop_analysis_to_console(shop):
    
    shop_name = shop[0]
    words_string = format_analysis_for_console(shop)
    print(f"Top 5 Words for {shop_name}:")
    print(words_string)
    print(" ")

def print_analysis_to_console(shops):
    """
    Prints the results of the analysis to the command line interface

    Parameters
    ----------
    shops : LIST OF LISTS
        Each entry is a list pair of a shop name and a list of the top words
        appearing in that shop's listings.

    Returns
    -------
    None.

    """
    for shop in shops:
        if shop[1]:
            print_shop_analysis_to_console(shop)
        else:
            cannot_find_shop_error(shop[0])

def cannot_find_shop_error(shop_name):
    """
    Prints an error to console when a provided shop is not found.

    Parameters
    ----------
    shop_name : STRING
        The name of the shop being analyzed.

    Returns
    -------
    None.

    """
    error_message = CANNOT_FIND_SHOP_ERROR_MESSAGE + shop_name
    print(error_message)

def default_analysis():
    """
    This is the default analysis for 10 selected Etsy shops.

    Returns
    -------
    None.

    """
    print(RUNNING_ANALYSIS_MESSAGE)
    shop_names = ['Element83',
                  'LDawningScott',
                  'PegandAwl',
                  'SinScissorsBoutique',
                  'OxAndPine',
                  'volaris',
                  'moderntextures',
                  'CarveCraftworks',
                  'EbanisteriaCavallaro',
                  'SheetMusicEphemera'
                  ]
    shops = get_shops_and_listings(shop_names)
    if shops:
        print_analysis_to_console(shops)
        print("The above are the top 5 terms for 10 different Etsy Shops")
    else:
        cannot_find_shop_error(shop_names)

def custom_analysis(shop_names):
    """
    Performs the analysis for shops input by the user.

    Parameters
    ----------
    shop_names : LIST OF STRINGS
        The names of the shops to be analyzed.

    Returns
    -------
    None.

    """
    print(RUNNING_ANALYSIS_MESSAGE)
    shops = get_shops_and_listings(shop_names)
    if shops:
        print_analysis_to_console(shops)
    else:
        cannot_find_shop_error(shop_names)


if __name__ == '__main__':
    input(WELCOME_MESSAGE)
    default_analysis_completed = False

    while not default_analysis_completed:
        try:
            default_analysis()
            default_analysis_completed = True
        except requests.exceptions.ConnectionError:
            input(CONNECTION_ERROR_MESSAGE)

    procedure_command = input(USER_PROMPT)

    while procedure_command.upper() != 'EXIT':
        if not procedure_command:
            print("No user input detected. Please try again.")
        else:
            try:
                custom_analysis([procedure_command])
            except TypeError:
                # this catches the error if a shop doesn't exist or otherwise
                # cannot be found
                print(CANNOT_FIND_SHOP_ERROR_MESSAGE)
            except requests.exceptions.ConnectionError:
                print(CONNECTION_ERROR_MESSAGE)
            procedure_command = input(USER_PROMPT)
