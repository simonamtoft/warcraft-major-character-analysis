import os
import re
from glob import glob
from tqdm import tqdm

import config


# create folder if it doesn't exist
if not os.path.exists(config.PATH_QUOTES):
    os.makedirs(config.PATH_QUOTES)


for fpath in tqdm(glob(config.PATH_CHARS + '*.txt'), desc='Extracting quotes'):
    charname = fpath.split('\\')[-1].replace('.txt', '').replace('_', ' ')

    # check if that file is already handled
    savepath = config.PATH_QUOTES + fpath.split('\\')[-1]
    # if os.path.isfile(savepath):
    #     continue

    # read file
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # check if has quotes section
    if not len(re.findall(r'[q|Q]uotes ?==', text)):
        continue
        
    # get only quotes
    quotes = re.split(r'[q|Q]uotes ?==', text)[-1]
    quotes = re.split(r'\s==([^=]+)==\s', quotes)[0]


    # remove stuff
    quotes = re.sub(r';.+\n', ' ', quotes)
    quotes = re.sub(r'==(.+)==', '', quotes)    # headers
    quotes = re.sub(r'\{\{[\w-]+\}\}', '', quotes)    #
    # Notes|Quotes|Transcript|Progress|Completion|Quest dialogue|Event Script|Will of the Ashbringer
    pattern = r'\{\{(?:Main|main)\|([\w ()/\'\!\,\?\-]+)(?:#[\w ]+)?\}\}'
    # notes = re.findall(pattern, quotes) # these might be able to be used
    quotes = re.sub(pattern, '', quotes)
    quotes = re.sub('</?br>', '\n', quotes)     # remove line breaks <br>
    quotes = re.sub('<ref [^<]+>', ' ', quotes) # remove start <ref>
    quotes = quotes.replace('</ref>', ' ')      # remove end <ref>
    
    # remove some specific chars
    for char in '*:': #<>"
        quotes = quotes.replace(char, ' ')           # remove specific chars

    # go over line by line
    lines = ''
    for line in quotes.split('\n'):
        line = line.strip()

        # extract quote from a text with character name {{text|--|person|quote}}
        text_quote = re.findall(r'\{\{(?:text|Text)\|(?:say|yell|whisper|Say|Yell)\|([^\|]+)\|([^\|]+)\}\}', line)
        if len(text_quote):
            character, line = text_quote[0]
            if character in charname or charname in character:
                line = line
            else:
                line = ''

        # extract quote from a text quote pattern {{text|--|quote}}
        text_quote = re.findall(r'\{\{(?:text|Text)\|(?:say|yell|whisper|Say|Yell)\|(.+)\}\}', line)
        if len(text_quote):
            line = text_quote[0]
        
        # remove character quotes that are from a different character
        character = re.findall(r'\'\'\'([\w ]+)\'\'\'', line)
        if len(character):
            character = character[0]
            if character in charname or charname in character:
                line = re.sub(r'\'\'\'([\w ]+)\'\'\'', ' ', line)
            else:
                line = ''
        
        # remove everything in <>
        line = re.sub(r'<[\w .\']+>', '', line)
        
        # don't add empty lines
        if line:
            line = line.strip()
            lines += line + '\n'

    # save file
    with open(savepath, 'w', encoding='utf-8') as f:
        f.write(lines)
