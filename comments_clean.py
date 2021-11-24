import os
import re
import json
from glob import glob
from tqdm import tqdm

import config


if __name__ == "__main__":

    # create destination folder if it doesn't exist
    if not os.path.exists(config.PATH_COMMENTS_CLEAN):
        os.makedirs(config.PATH_COMMENTS_CLEAN)
    
    # convert all comments on each character to text pages
    for char_path in tqdm(glob(config.PATH_COMMENTS + '*.njson'), desc='Processing wowhead comments to fulltext'):
        # check if that file is already handled
        savepath = config.PATH_COMMENTS_CLEAN + char_path.split('\\')[-1].replace('njson', 'txt')
        if os.path.isfile(savepath):
            continue
    
        # extract all comments from the downloaded character comments from wowhead
        text = ''
        for comment_meta in open(char_path, 'r', encoding='utf-8'):
            text += ' ' + json.loads(comment_meta)['body']

        # clean brackets and newlines/tabs
        text = re.sub(r"\[.+?\]", " ", text)
        text = re.sub(r"[\t\n]+", " ", text)

        # write text to txt file
        with open(savepath, 'w', encoding="utf-8") as f:
            f.write(text)