import os
import re
import json
import nltk
from glob import glob
from tqdm import tqdm

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

    # create destination folder if it doesn't exist
    if not os.path.exists(config.PATH_COMMENTS_WORDS):
        os.makedirs(config.PATH_COMMENTS_WORDS)

    # convert all comments on each character to words
    for char_path in tqdm(glob(config.PATH_COMMENTS + '*.njson'), desc='Processing wowhead comments'):

        # check if that file is already handled
        savepath = config.PATH_COMMENTS_WORDS + char_path.split('\\')[-1].replace('njson', 'txt')
        if os.path.isfile(savepath):
            continue
        
        # extract all comments from the downloaded character comments from wowhead
        text = ''
        for comment_meta in open(char_path, 'r', encoding='utf-8'):
            text += ' ' + json.loads(comment_meta)['body']

        # clean brackets and newlines/tabs
        text = re.sub(r"\[.+?\]", " ", text)
        text = re.sub(r"[\t\n]+", " ", text)

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