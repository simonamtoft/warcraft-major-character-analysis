from types import GenericAlias
import nltk
import os
import sys
import pickle
import argparse
import community
from glob import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn.categorical import factorplot
sns.set()

import networkx as nx

import config
from text_helpers import disp_wordcloud


def get_top(col, split, n_top):
    words = col[split]['words']
    tfidf = col[split]['tf'] * col[split]['idf']
    top = ', '.join(words[np.argsort(tfidf)[::-1]][:n_top])
    return top


# get source as input argument from CLI
parser = argparse.ArgumentParser(description='Perform text analysis on either wowpedia or wowhead comments. Default wowpedia.')
parser.add_argument('-s', '--source', help='Source of text to process (wowpedia/wowhead)', default='wowpedia', choices=['wowpedia', 'wowhead'])
args = parser.parse_args()
source = args.source
PATH_RES = config.PATH_RES + source + '/'
PATH_PLOTS = config.PATH_PLOTS + source + '/'

# save this at end
OUT_STRING = ''

# check that everything is ran before this
if not os.path.isfile(config.PATH_RES + 'Gcc_wow.gexf'):
    print('Error: Graph and DataFrame not created. Please run script "create_wow_graph.py".')
    sys.exit(1)

# load graph as undirected
Gcc = nx.read_gexf(config.PATH_RES + 'Gcc_wow.gexf').to_undirected()

# read in character DataFrame
df = pd.read_csv(config.PATH_RES + 'df_chars.csv')

# create communities if not done already, otherwise load
filename = config.PATH_RES + 'Communities.json'
if not os.path.isfile(filename):
    print('Creating new community partition.')
    partition = community.best_partition(Gcc)
    communities = []
    for p in set(partition.values()):
        names = [n for n in partition if partition[n] == p]
        communities.append(names)
    pickle.dump(communities, open(filename, 'wb'))
    print(f'Saved as pickle {filename}')
else: 
    print('Loading existing community partition.')
    print(f'from pickle {filename}')
    communities = pickle.load(open(filename, 'rb'))

# get top chars in each community
degs = list(Gcc.degree())
com_names = []
for com in communities:
    com_sorted = sorted([(n, v) for n, v in degs if n in com], key=lambda x: x[1], reverse=True)
    top_names = [n for n, _ in com_sorted[:3]]
    com_name = ', '.join(top_names)
    com_names.append(com_name)

# define what to look into
attr_lookup = {
    'Gender': [('Male', '#0B1C51'), ('Female', '#FCB9B2')],
    'Faction': [('Alliance', config.COLOR_ALLIANCE), ('Horde', config.COLOR_HORDE)]
}

# display top words for attributes
for attr in attr_lookup:
    OUT_STRING += f'\n\nTop 5 for attribute {attr}'
    col = pickle.load(open(PATH_RES + attr + '_dict.json', 'rb'))
    for split, _ in attr_lookup[attr]:
        top = get_top(col, split, 5)
        OUT_STRING += f'\n\t{split}: {top}'

# display top words per community
OUT_STRING += '\n\n========================================================\n\n'
OUT_STRING += 'Top 5 words for each community'
col = pickle.load(open(PATH_RES + 'Louvain_dict.json', 'rb'))
for i, com_name in enumerate(com_names):
    OUT_STRING += f'\n\n"{com_name}"'
    OUT_STRING += '\n' + get_top(col, i, 5)

OUT_STRING += '\n\n========================================================\n\n'

# save results to text file
with open(PATH_RES + 'text_analysis_results.txt', 'w') as f:
    f.write(OUT_STRING)

# create wordclouds for attributes
for attr in attr_lookup:
    col = pickle.load(open(PATH_RES + attr + '_dict.json', 'rb'))
    for split, color in attr_lookup[attr]:
        filename = PATH_PLOTS + f'wc_{split}.png'
        maskpath = f'./data/masks/{split}.jpg'
        if not os.path.isfile(maskpath):
            maskpath = ''
        disp_wordcloud(
            split, col,
            savepath=filename, 
            maskpath=maskpath, 
            contour_color=None,
            contour_width=0
        )

# create wordclouds for communities
col = pickle.load(open(PATH_RES + 'Louvain_dict.json', 'rb'))
for i, com_name in enumerate(com_names):
    filename = PATH_PLOTS + f'wc_com_{i}.png'
    disp_wordcloud(
        i, col,
        savepath=filename,
        contour_color=None,
        contour_width=0
    )
