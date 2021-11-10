from glob import glob
import requests
from tqdm import tqdm
import json
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path

# this script requires "download_character_pages.py" to already have been executed

Path("data/char_comments").mkdir(parents=True, exist_ok=True)

base_url = 'https://wowhead.com'
search_url = f"{base_url}/npcs"

for fn in tqdm(
    glob('data/wow_chars/*.txt'),
    desc='Fetching comment data'
):
    raw_char_name = fn.split('\\')[-1][:-4]
    char_name = raw_char_name.replace('_', ' ')

    page = requests.get(f"{search_url}/name:{char_name.replace(' ','+')}?filter=33;1;0")
    
    soup = BeautifulSoup(page.text, 'html.parser')
    raw_text = soup.find("div", { "id": "lv-npcs" })
    if not raw_text:
        # print('Skipped %s (0 results)' % char_name)
        continue
        
    raw_text = raw_text.find_next('script').text
    raw_text = re.sub(
        r"Listview\.extraCols\.(\w+)",
        r'"\1"',
        raw_text[14:-3]
    )
    listview = json.loads(raw_text)

    npcs = list(filter(
        lambda c: char_name in c.get('name', ''),
        listview.get('data', [])
    ))
    
    # print('Fetching comments for %d pages for %s' % (len(npcs), char_name))
    char_comments = []
    
    for npc in npcs:
        npc_id = npc.get('id')
        comments_page = requests.get(f"{base_url}/npc={npc_id}#comments")
        comments_soup = BeautifulSoup(comments_page.text, 'html.parser')
        comments_script = next(script for script in comments_soup.find_all('script') if 'lv_comments0' in script.text)
        comments_start_idx = comments_script.text.index('lv_comments0 = ')


        raw_comments = json.loads(comments_script.text[(comments_start_idx+15):-2])
        for comment in raw_comments:
            char_comments.append(comment)

    with open(f'data/char_comments/{raw_char_name}.njson', 'w') as f:
        f.write('\n'.join(json.dumps(c) for c in char_comments))

    
    time.sleep(5)