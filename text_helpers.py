import nltk
import pickle
import numpy as np
from PIL import Image
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

FONT_PATH = "./store/NeoSans Black.otf"


def init_collection(df, attr, path_words, words_corpus):
    """Initialize a collection based on an attribute in the DataFrame.
        The 'collection' will consists of the collection of words from the
        given word_corpus split by the attribute."""
    
    # get unique attributes
    attrs = df[attr].unique()

    # create collection with texts for each member
    col = {}
    for at in attrs:
        # create list of paths for every character of current attribute
        names = df.loc[df[attr] == at, 'Name'].values
        paths = [
            path_words + n.replace(' ', '_') + '.txt' 
            for n in names
        ]

        # save text for attribute
        col[at] = {'text': nltk.Text(words_corpus.words(paths))}
    return col


def populate_collection(col, save_path=''):
    """Calculate TC, TF, IDF, TC-IDF, TF-IDF and wordcloud string and add to collection."""
    N = len(col)
    for split in tqdm(col, desc='Computing values'):
        text = col[split]['text']

        # calculate TC and TF
        words, tc = np.unique(text, return_counts=True)
        tf = tc / len(text)

        # calculate IDF
        idf = []
        for word in words:
            n_t = 0
            for doc in col:
                txt = col[doc]['text']
                if txt.count(word):
                    n_t += 1
            idf.append(np.log(N / n_t))

        # store values
        col[split]['words'] = words
        col[split]['tc'] = tc
        col[split]['tf'] = tf
        col[split]['idf'] = idf
        col[split]['tcidf'] = tc * idf
        col[split]['tfidf'] = tf * idf

    # create wordcloud for each
    for split in tqdm(col, desc='Computing wordclouds'):
        # calculate number of reps based on TC-IDF
        reps = (col[split]['tcidf']).astype(int)

        # create wordcloud string based on number of reps
        words_repeated = ''
        for idx, w in enumerate(col[split]['words']):
            w_rep = (str(w) + ' ') * int(reps[idx])
            words_repeated += w_rep
        col[split]['wordcloud'] = words_repeated
    
    if save_path != '':
        with open(save_path, 'wb') as f:
            pickle.dump(col, f)
    
    return col


def disp_wordcloud(col_idx, collection, maskpath='', savepath='', title='', figsize=None):
    if collection[col_idx]['wordcloud'] == '':
        return -1

    plt.figure(figsize=figsize)

    # load mask
    mask = None
    if maskpath != '':
        mask = np.asarray(Image.open(maskpath))
    else:
        plt.title(title, fontsize=14)

    wc = (
        WordCloud(
            max_words=1000, 
            margin=1,
            collocations=False, 
            mask=mask,
            background_color="rgba(255, 255, 255, 0)", 
            mode="RGBA",
            font_path=FONT_PATH,
            colormap='Dark2',
        )
        .generate(collection[col_idx]['wordcloud'])
        .to_array()
    )
    
    plt.imshow(wc, interpolation="bilinear")
    if title != '':
        prop = fm.FontProperties(fname=FONT_PATH)
        plt.title(title, fontproperties=prop)
    plt.axis("off")
    if savepath != '':
        plt.savefig(savepath, transparent=False, dpi=500)
        plt.close()
    else:
        plt.show()


def get_paths(df, attr, val, source='wowpedia'):
    """Get paths to the clean text files for either wowhead or wowpedia for a specific partition of the network."""
    if source == 'wowhead':
        folder = 'char_comments_clean/'
    elif source == 'wowpedia':
        folder = 'wow_chars_clean/'
    return ['./data/' + folder + name.replace(' ', '_') + '.txt' for name in df[df[attr] == val]['Name'].values]

