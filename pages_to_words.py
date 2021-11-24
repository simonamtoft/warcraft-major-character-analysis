import os
import re
import json
import nltk
from glob import glob

import config


def should_keep(token, remove_words=[]):
    """ Determine if token should be kept in final word list.
        Excludes non-words and words in remove_words."""
    if token.isalpha():
        if token not in remove_words:
            return True
    return False


if __name__ == "__main__":
    # define tokenizer and lemmatizer
    wpt = nltk.tokenize.WordPunctTokenizer()
    wnl = nltk.stem.wordnet.WordNetLemmatizer()

    # define words/tokens to remove
    remove_words = nltk.corpus.stopwords.words('english')

    # create folder if it doesn't exist
    if not os.path.exists(config.PATH_WORDS):
        os.makedirs(config.PATH_WORDS)
    
    # create word file for each cleaned character page
    for fpath in glob(config.PATH_CLEAN + '*.txt'):
        # check if that file is already handled
        savepath = config.PATH_WORDS + fpath.split('\\')[-1]
        if os.path.isfile(savepath):
            continue

        # read in cleaned character text file
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        # remove stuff regarding patches
        text = re.sub(r'Patch \d.\d.\d \(\d\d\d\d\-\d\d\-\d\d\)\:', ' ', text)
        
        # butcher contractions (')
        # important to keep meaning for e.g. "A'dal" and "Sha'tar"
        text = text.replace("'", "").lower()

        # tokenize text
        tokens = wpt.tokenize(text)

        # Keep only tokens that are words, and lemmatize them
        words = [wnl.lemmatize(t) for t in tokens if should_keep(t, remove_words)]
        
        # write words to txt file
        with open(savepath, 'w', encoding="utf-8") as f:
            for w in words:
                f.write("%s\n" % w)
