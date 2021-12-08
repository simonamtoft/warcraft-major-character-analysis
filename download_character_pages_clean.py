import os
import re
import json
from glob import glob
from tqdm import tqdm
from api import generate_query, get_response_from, get_plaintext_from

import config

if __name__ == "__main__":
    # create folder if it doesn't exist
    if not os.path.exists(config.PATH_CLEAN):
        os.makedirs(config.PATH_CLEAN)

    # download every plain text character file from the wiki
    for fname in tqdm(glob('data/wow_chars/*.txt'), desc='Downloading clean character pages'):
        # get charname from path
        charname = fname.replace('.txt', '').split('\\')[-1]

        # get savepath
        savepath = config.PATH_CLEAN + charname + '.txt'
        if os.path.exists(savepath):
            continue

        query = generate_query(
            config.URL_BASE, charname,
            content='prop=extracts&exlimit=1&explaintext'
        )

        # get response from API
        response = get_response_from(query)

        # extract text from respone
        text = get_plaintext_from(response)

        # do some additional cleaning
        text = re.sub(r'==(.+)==', '', text)    # remove headers
        text = re.sub(r'\n+', ' ', text)        # remove newline
        text = re.sub(r'\t+', ' ', text)        # remove tabs
        text = re.sub(r'\s+', ' ', text)         # remove excess spaces

        # save cleaned character text file
        with open(savepath, "w", encoding="utf-8") as f:
            json.dump(text, f, ensure_ascii=False)

    print(f'Downloaded and cleaned {len(glob(config.PATH_CLEAN + "*.txt"))} character pages')