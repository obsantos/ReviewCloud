#!/usr/bin/env python

'''
    Script to generate a word cloud using your app's reviews from Play Store
    Author: Omar Busto Santos 
    Date created: 08/05/2020
'''

import argparse
import pandas as pd 

def parse_report(path):
    """Parses the report (.csv) file , filters and generates a DataFrame"""
    # Read the report in utf16
    df = pd.read_csv(path, encoding="utf16")

    # Optional - Filter by english reviews. Word Count has a list of words to ignore, but only in english
    filtered = df.loc[df['Reviewer Language'] == 'en'].copy()

    # Drop rows with NaN review text
    filtered.dropna(subset = ['Review Text'], inplace=True)

    # Extract words of every review in the report
    words = extract_words_from_report(filtered)  
    # print(words)

def extract_words_from_report(df):
    """Extracts the words of each review in the whole report and returns a list"""
    return [extract_words_from_review(review) for review in df['Review Text']]


def extract_words_from_review(review):
    """Extracts the words of a given review, filters them and returns a list"""
    filteredWords = review.split()
    print(filteredWords)

def main():
    parser = argparse.ArgumentParser(description='Script to generate a word cloud from a Play Store review report (.csv)')
    parser.add_argument('-rp','--report-path', metavar='<Path where the report is located>', type=str, required=True)
    args = parser.parse_args()
    parse_report(args.report_path)

if __name__ == '__main__':
    main()