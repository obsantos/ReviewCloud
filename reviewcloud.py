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
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import multidict as multidict
import re

stopwords = set(STOPWORDS)

def parse_report(path, language):
    """Parses the report (.csv) file , filters and generates a DataFrame"""
    # Read the report in utf16
    report = pd.read_csv(path, encoding="utf16", dtype=object)

    # Optional - Filter by language. Word Cloud has a list of words to ignore, but only in english
    if language is not None:
        report = report.loc[report['Reviewer Language'] == language].copy()

    # Drop rows with NaN review text
    report.dropna(subset = ['Review Text'], inplace=True)

    # Extract words of every review in the report
    words = [extract_words_from_review(review) for review in report['Review Text']]

    # Concat the list of lists
    concat = reduce(operator.concat, words)
    
    return concat

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

def getFrequencyDictForText(sentence):
    """Creates a multidict with the words and their frequency"""
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for text in sentence.split(" "):
        if text in stopwords:
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def create_word_cloud(words, output, unique):
    """Creates a word cloud and shows it"""
    # Create WordCloud instance
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10)

    # Generate the word cloud based on mode
    if unique:         
        wordcloud.generate_from_frequencies(getFrequencyDictForText(" ".join(words))) 
    else:
        wordcloud.generate(" ".join(words))
  
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0)

    if output is not None:
        plt.savefig(output)
    else:        
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Script to generate a word cloud from a Play Store review report (.csv)')
    parser.add_argument('-rp','--report-path', help='Path where the comma separated report (.csv) is located', type=str, required=True)
    parser.add_argument('-lang','--language', help='Optional. Language code to filter reviews (i.e "en", "es"...)', type=str, required=False)
    parser.add_argument('-out','--output', help='Optional. Path to the file where to save word cloud', type=str, required=False)
    parser.add_argument('-uniq','--unique', help='Optional. Use high frequency unique words. If omitted it uses high frequency words ignoring singular/plurals (i.e "car" and "cars" count as same word)', action='store_true', required=False)
    args = parser.parse_args()

    # Obtain all words in the reviews
    words = parse_report(args.report_path, args.language)

    # Create and plot the word cloud
    create_word_cloud(words, args.output, args.unique)

if __name__ == '__main__':
    main()