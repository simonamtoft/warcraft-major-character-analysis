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
    parser = argparse.ArgumentParser(description=f"Convert pages from {config.PATH_CLEAN} to list of processed words ready for text analysis, stored in {config.PATH_WORDS}.")
    parser.add_argument('-f', dest='force', action='store_true')
    parser.set_defaults(force=False)
    args = parser.parse_args()

    # define tokenizer and lemmatizer
    wpt = nltk.tokenize.WordPunctTokenizer()
    wnl = nltk.stem.wordnet.WordNetLemmatizer()

    # define words/tokens to remove
    remove_words = nltk.corpus.stopwords.words('english')
    remove_words += ['patch', 'player']

    # create folder if it doesn't exist
    if not os.path.exists(config.PATH_WORDS):
        os.makedirs(config.PATH_WORDS)
    
    # create word file for each cleaned character page
    files = glob(config.PATH_CLEAN + '*.txt')
    characters = [f.split('\\')[-1].replace('.txt', '').replace('_', ' ') for f in files]
    for fpath in tqdm(files, desc='Convert clean files to list of words'):
        savepath = config.PATH_WORDS + fpath.split('\\')[-1]
        
        # check if that file is already handled
        if not args.force:
            if os.path.isfile(savepath):
                continue

        # read in cleaned character text file
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        # remove stuff regarding patches
        text = re.sub(r'Patch \d.\d.\d \(\d\d\d\d\-\d\d\-\d\d\)\:', ' ', text)

        # remove character names from text
        for character in characters:
            text = text.replace(character, ' ')
        
        # butcher contractions (')
        # important to keep meaning for e.g. "Sha'tar"
        text = text.replace("'", "")
        
        # lower text
        text = text.lower()

        # tokenize text
        tokens = wpt.tokenize(text)

        # Keep only tokens that are words, and lemmatize them
        words = [wnl.lemmatize(t) for t in tokens if should_keep(t, remove_words)]
        
        # write words to txt file
        with open(savepath, 'w', encoding="utf-8") as f:
            for w in words:
                f.write("%s\n" % w)
