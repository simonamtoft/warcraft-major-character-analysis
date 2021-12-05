import os
import pickle
import argparse
import seaborn as sns
sns.set()

import config
from text_helpers import disp_wordcloud

# get source as input argument from CLI
parser = argparse.ArgumentParser(description='Perform text analysis on either wowpedia or wowhead comments. Default wowpedia.')
parser.add_argument('-s', '--source', help='Source of text to process (wowpedia/wowhead)', default='wowpedia', choices=['wowpedia', 'wowhead'])
args = parser.parse_args()
source = args.source
PATH_RES = config.PATH_RES + source + '/'
PATH_PLOTS = config.PATH_PLOTS + source + '/'

print(f'Creating Wordclouds for {source}')

# define what to look into
attr_lookup = {
    'Gender': ['Male', 'Female', 'Unknown'],
    'Faction': ['Alliance', 'Horde'],
    'Status': ['Alive', 'Deceased']
}

# create wordclouds for attributes
for attr in attr_lookup:
    col = pickle.load(open(PATH_RES + attr + '_dict.json', 'rb'))
    for split in attr_lookup[attr]:
        filename = PATH_PLOTS + f'wc_{split}.png'
        
        # get mask if present
        maskpath = f'./store/masks/{split}.jpg'
        if not os.path.isfile(maskpath):
            maskpath = ''
        
        disp_wordcloud(
            split, col,
            title=source.title(),
            savepath=filename, 
            maskpath=maskpath, 
        )

# create wordclouds for communities
col = pickle.load(open(PATH_RES + 'Louvain_dict.json', 'rb'))
for i in range(len(col)):
    filename = PATH_PLOTS + f'wc_com_{i}.png'
    
    # get mask if present
    maskpath = f'./store/masks/com_mask_{i}.jpg'
    if not os.path.isfile(maskpath):
        maskpath = ''
            
    disp_wordcloud(
        i, col,
        title=source.title(),
        savepath=filename, 
        maskpath=maskpath, 
    )
