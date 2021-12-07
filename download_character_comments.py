## IMPORTANT
## This script requires "download_character_pages.py" to already have been executed, as it required the character page text files to be present

from glob import glob
import requests
from tqdm import tqdm
import json
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path
import os

import config

# ensure output directory exists
Path(config.PATH_COMMENTS).mkdir(parents=True, exist_ok=True)

# wowhead URLs
base_url = 'https://wowhead.com'
search_url = f"{base_url}/npcs"


# process one character at a time (using the wikipages character list as reference)
for fn in tqdm(
    glob(config.PATH_CHARS + '*.txt'),
    desc='Fetching comment data'
):
    # obtain the original character name from the path name
    raw_char_name = os.path.basename(fn)[:-4]
    char_name = raw_char_name.replace('_', ' ') # fix spaces

    # get wowhead query page
    page = requests.get(f"{search_url}/name:{char_name.replace(' ','+')}?filter=33;1;0")
    
    # init HTML parser (virtual dom)
    soup = BeautifulSoup(page.text, 'html.parser')

    # find specific div element containing list of NPCs
    raw_text = soup.find("div", { "id": "lv-npcs" })
    if not raw_text:
        continue

    # we'll find the exact character details embedded in a script tag        
    raw_text = raw_text.find_next('script').text
    raw_text = re.sub(
        r"Listview\.extraCols\.(\w+)",
        r'"\1"',
        raw_text[14:-3]
    )
    # we parse some JSON from the script tag
    listview = json.loads(raw_text)

    # remove NPC pages that do not include the character name we retrieved earlier
    npcs = list(filter(
        lambda c: char_name in c.get('name', ''),
        listview.get('data', [])
    ))
    
    # collect comments in this list
    char_comments = []

    # we gather for all filtered NPC pages 
    for npc in npcs:
        npc_id = npc.get('id')

        # we fetch the wowhead NPC page
        comments_page = requests.get(f"{base_url}/npc={npc_id}#comments")
        # another virtual DOM
        comments_soup = BeautifulSoup(comments_page.text, 'html.parser')
        # again, the information we are seeking is embedded in a script tag
        comments_script = next(script for script in comments_soup.find_all('script') if 'lv_comments0' in script.text)
        comments_start_idx = comments_script.text.index('lv_comments0 = ')
        # again, we parse JSON from the script tag (the offsets here are very important)
        raw_comments = json.loads(comments_script.text[(comments_start_idx+15):-2])
        for comment in raw_comments:
            # add comments to the collection
            char_comments.append(comment)

    # write all character comments as newline-delimited JSON
    with open(f'{config.PATH_COMMENTS}{raw_char_name}.njson', 'w') as f:
        f.write('\n'.join(json.dumps(c) for c in char_comments))

    # sleep for 5 seconds to avoid being blacklisted by wowhead for sending too many requests
    time.sleep(5)