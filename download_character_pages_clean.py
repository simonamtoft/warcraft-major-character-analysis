import os
import re
import json
from glob import glob
from api import generate_query, get_response_from, get_plaintext_from

# define base API url
URL_BASE = 'https://wowpedia.fandom.com/api.php'

# define where to save cleantext character pages
SAVE_FOLDER = './data/wow_chars_clean/'


if __name__ == "__main__":
    for fname in glob('data/wow_chars/*.txt'):
        # get charname from path
        charname = fname.replace('.txt', '').split('\\')[-1]

        # get savepath
        savepath = SAVE_FOLDER + charname + '.txt'
        if os.path.exists(savepath):
            continue

        query = generate_query(
            URL_BASE, charname,
            content='prop=extracts&exlimit=1&explaintext'
        )

        # get response from API
        response = get_response_from(query)

        # extract text from respone
        text = get_plaintext_from(response)

        # do some additional cleaning
        text = re.sub(r'==(.+)==', '', text)        # remove headers
        text = re.sub('[\n\t]+', ' ', text)         # remove newline + tabs
        text = re.sub('\[[\w\d\-]+\]', ' ', text)   # remove stuff in brackets []
        text = re.sub('\s+', ' ', text)             # remove excess spaces

        # save cleaned character text file
        with open(savepath, "w", encoding="utf-8") as f:
            json.dump(text, f, ensure_ascii=False)

    print(f'Downloaded and cleaned {len(glob(SAVE_FOLDER + "*.txt"))} character pages')