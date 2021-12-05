import os
import re
import json
import nltk
from glob import glob
from tqdm import tqdm
import argparse

import config


def should_keep(token, remove_words=[]):
    """ Determine if token should be kept in final word list.
        Excludes non-words and words in remove_words."""
    if token.isalpha():
        if token not in remove_words:
            return True
    return False


if __name__ == "__main__":
    # add argument parser
    parser = argparse.ArgumentParser(description=f"Convert pages from to list of processed words ready for text analysis.")
    parser.add_argument('-f', dest='force', action='store_true')
    parser.set_defaults(force=False)
    parser.add_argument('-s', '--source', help='Source of text to process (wowpedia/wowhead)', default='wowpedia', choices=['wowpedia', 'wowhead'])
    args = parser.parse_args()

    # determine paths based on source
    if args.source == 'wowhead':
        path_clean = config.PATH_COMMENTS_CLEAN
        path_words = config.PATH_COMMENTS_WORDS
    else:
        path_clean = config.PATH_CLEAN
        path_words = config.PATH_WORDS
    
    # create folder if it doesn't exist
    if not os.path.exists(path_words):
        os.makedirs(path_words)

    # define tokenizer and lemmatizer
    wpt = nltk.tokenize.WordPunctTokenizer()
    wnl = nltk.stem.wordnet.WordNetLemmatizer()

    # get list of files
    files = glob(path_clean + '*.txt')

    # create list of character names
    characters = [
        f.split('\\')[-1].replace('.txt', '').replace('_', ' ').split(' (')[0].lower().replace("'", '')
        for f in files
    ]
    # remove uncommon characters that could also be normal words from list
    for ch in ['zul', 'tyr', 'ra']:
        characters.remove(ch)

    # define words/tokens to remove
    remove_words = nltk.corpus.stopwords.words('english')
    remove_words += ['patch', 'player']
    
    # create word file for each cleaned character page
    for fpath in tqdm(files, desc=f'Convert clean {args.source} files to list of words'):
        savepath = path_words + fpath.split('\\')[-1]
        
        # check if that file is already handled
        if not args.force:
            if os.path.isfile(savepath):
                continue

        # read in cleaned character text file
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        # remove stuff regarding patches
        text = re.sub(r'Patch \d.\d.\d \(\d\d\d\d\-\d\d\-\d\d\)\:', ' ', text)
        
        # butcher contractions (')
        # important to keep meaning for e.g. "Sha'tar"
        text = text.replace("'", "")
        
        # lower text
        text = text.lower()

        # remove character names
        for char in characters:
            text = re.sub(char, ' ', text)

        # tokenize text
        tokens = wpt.tokenize(text)

        # Keep only tokens that are words, and lemmatize them
        words = [wnl.lemmatize(t) for t in tokens if should_keep(t, remove_words)]
        
        # write words to txt file
        with open(savepath, 'w', encoding="utf-8") as f:
            for w in words:
                f.write("%s\n" % w)
