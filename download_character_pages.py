import re
import os
from glob import glob
from api import generate_query, get_response_from, get_main_from

import config


# define linking pattern for specific fandom site
# following works for Major characters on the wowpedia
CHAR_LINK_PATTERN = r'\[\[(.*?)(?:[\|#].*?)?\]\]'


if __name__ == "__main__":
    # generate query and get response from API
    query = generate_query(config.URL_BASE, config.START_TITLE)
    response = get_response_from(query)

    # get txt from response dict
    txt = get_main_from(response)

    # remove everything before races
    txt = txt.split('==[[Races]]==')[1]

    # remove all headers
    txt = re.sub(r'==(.+)==', '', txt)

    # remove last part of page
    txt = txt.split('{{Main characters}}')[0]

    # get list of all main characters
    charnames = re.findall(CHAR_LINK_PATTERN, txt)
    print(f'Found {len(charnames)} characters')

    # download each character page
    for charname in charnames:
        # get name of page from charname
        pagename = charname.replace(' ', '_')
        filename = config.PATH_CHARS + pagename + '.txt'

        # skip already downloaded files
        if os.path.isfile(filename):
            continue
        
        # Get character page from API
        query = generate_query(config.URL_BASE, pagename)
        response = get_response_from(query)
        txt = get_main_from(response)

        # we know all redirect pages are also mentioned as the real page
        if '#REDIRECT' in txt or '#redirect' in txt:
            continue

        # save character page as file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(txt)
    print(f'Downloaded {len(glob(config.PATH_CHARS + "*.txt"))} character pages')
