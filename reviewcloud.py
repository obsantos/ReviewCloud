#!/usr/bin/env python

'''
    Script to generate a word cloud using your app's reviews from Play Store
    Author: Omar Busto Santos 
    Date created: 08/05/2020
'''

import string
import emoji
import argparse
import pandas as pd 
from functools import reduce
import operator

def parse_report(path):
    """Parses the report (.csv) file , filters and generates a DataFrame"""
    # Read the report in utf16
    df = pd.read_csv(path, encoding="utf16")

    # Optional - Filter by english reviews. Word Cloud has a list of words to ignore, but only in english
    filtered = df.loc[df['Reviewer Language'] == 'en'].copy()

    # Drop rows with NaN review text
    filtered.dropna(subset = ['Review Text'], inplace=True)

    # Extract words of every review in the report
    words = [extract_words_from_review(review) for review in filtered['Review Text']]

    # Concat the list of lists
    concat = reduce(operator.concat, words)
    print(len(concat))

def extract_words_from_review(review):
    """Extracts the words of a given review, filters them and returns a list"""
    # Get the list of words using spacing as separation
    splitWords = review.split()

    # Clean up the words removing extra characters
    cleanWords = [clean_words(word) for word in splitWords]

    # Filter out words we don't want to show
    filteredWords = list(filter(filter_words, cleanWords))

    return filteredWords

def clean_words(word):
    """Cleans up the words removing extra characters like punctuations, emojis, etc """    
    # Remove punctuation symbols
    punctuation_free = word.translate(str.maketrans('', '', string.punctuation))

    # Remove emojis
    emoji_free = emoji.get_emoji_regexp().sub(u'', punctuation_free)

    # Turn into lower caps
    lower = emoji_free.lower()

    return lower

def filter_words(word):
    """Applies some filtering and discard words based on certain rules"""
    if (len(word) > 1):
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description='Script to generate a word cloud from a Play Store review report (.csv)')
    parser.add_argument('-rp','--report-path', metavar='<Path where the report is located>', type=str, required=True)
    args = parser.parse_args()
    parse_report(args.report_path)

if __name__ == '__main__':
    main()