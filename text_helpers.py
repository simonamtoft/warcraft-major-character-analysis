import nltk
import pickle
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import config

def init_collection(df, attr, words_corpus):
    # get unique attributes
    attrs = df[attr].unique()

    # create collection with texts for each member
    col = {}
    for at in attrs:
        # create list of paths for every character of current faction
        names = df.loc[df[attr] == at, 'Name'].values
        paths = [
            config.PATH_WORDS + n.replace(' ', '_') + '.txt' 
            for n in names
        ]

        # save text for faction
        col[at] = {'text': nltk.Text(words_corpus.words(paths))}
    return col


def add_col_values(df, col, attr, save=False):
    N = len(col)
    for split in col:
        text = col[split]['text']

        # calculate TC and TF
        words, tc = np.unique(text, return_counts=True)
        tf = tc / len(text)

        # calculate IDF
        IDF = []
        for word in words:
            n_t = 0
            for doc in col:
                txt = col[doc]['text']
                if txt.count(word):
                    n_t += 1
            IDF.append(np.log(N / n_t))

        # store stuff
        col[split]['words'] = words
        col[split]['tc'] = tc
        col[split]['tf'] = tf
        col[split]['idf'] = tf
    
    if save:
        with open(config.PATH_RES + attr + '_dict.json', 'wb') as f:
            pickle.dump(col, f)
    return col


def add_wordcloud_string(col):
    for split in col:
        cs = col[split]
        reps = 100 * (cs['tc'] * cs['idf']).astype(int)

        words_repeated = ''
        for idx, w in enumerate(cs['words']):
            w_rep = (str(w) + ' ') * int(reps[idx])
            words_repeated += w_rep

            col[split]['wordcloud'] = words_repeated
    return col 


def disp_wordcloud(col_idx, collection, savepath=''):
    if collection[col_idx]['wordcloud'] == '':
        return -1
    wc = (
        WordCloud(
            max_words=1000,  margin=1, collocations=False)
        .generate(collection[col_idx]['wordcloud'])
        .to_array()
    )
    plt.title(col_idx)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    if savepath != '':
        plt.savefig(savepath)
    plt.show()