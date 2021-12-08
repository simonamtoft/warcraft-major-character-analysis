import os
import re
from glob import glob
from tqdm import tqdm

import config

def nickname_map(charname):
    """Nickname map that is needed when comparing character names in quotes."""
    if charname == 'The Banshee Queen':
        return 'Sylvanas'
    elif charname == 'High Overlord Saurfang':
        return 'Varok'
    elif 'Ashara' in charname:
        return charname.replace('Ashara', 'Azshara')
    elif 'Manstorm' in charname:
        return charname.replace('Manstorm', 'Manastorm')
    elif charname == 'Prince Llane Wrynn':
        return 'Llane Wrynn I'
    elif 'Halduron' in charname:
        return 'Halduron Brightwing'
    elif 'Mekkatorque' in charname:
        return 'Gelbin Mekkatorque'
    elif charname == 'Spiritwalker Ebonhorn':
        return 'Ebyssian'
    return charname


# create folder if it doesn't exist
if not os.path.exists(config.PATH_QUOTES):
    os.makedirs(config.PATH_QUOTES)


for fpath in tqdm(glob(config.PATH_CHARS + '*.txt'), desc='Extracting quotes'):
    charname = fpath.split('\\')[-1].replace('.txt', '').replace('_', ' ')

    # check if that file is already handled
    savepath = config.PATH_QUOTES + fpath.split('\\')[-1]
    # if os.path.isfile(savepath):
    #     continue

    # Dentarg is a reference page, took out manually
    if charname == 'Dentarg':
        continue
    
    # read file
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # check if has quotes section
    if not len(re.findall(r'[q|Q]uotes ?==', text)):
        continue
        
    # extract the quotes section from the wikipage
    quotes = re.split(r'[q|Q]uotes ?==', text)[-1]
    quotes = re.split(r'\s==([^=]+)==\s', quotes)[0]

    # remove gallery section
    quotes = re.sub(r'<gallery>[^><]+<\/gallery>', ' ', quotes)
    
    # remove refs
    quotes = re.sub(r'<ref>[^<]+<\/ref>', ' ', quotes)
    quotes = re.sub(r'<ref name=[\w\d \-"\'().,]+>.+<\/ref>', ' ', quotes)
    quotes = re.sub(r'<ref name=[\w\d \-"\'().,]+\/>', ' ', quotes)

    # remove stuff
    quotes = re.sub(r'==(.+)==', '', quotes)                # headers
    quotes = re.sub(r'\{\{\w+\-section\}\}', '', quotes)    # section headers
    quotes = re.sub('</?br>', '\n', quotes)                 # remove line breaks <br>
    quotes = re.sub('\{\{sic\}\}', '', quotes)              # remove {{sic}}

    # remove references to patches
    quotes = re.sub(r'\(Patch \d(.\d)+\)', ' ', quotes)
    quotes = re.sub(r"\(Removed in ''Patch \d.\d.\d\w?''\)", '', quotes)

    # remove actual url links
    urls = re.findall(r'\[(https?:\/\/[\w\/.]+)(.+)\]', quotes)
    for url in urls:
        quotes = quotes.replace(
            '[' + url[0] + url[1] + ']',
            url[1]
        )

    # remove specific chars that appear at the start of a lot of lines
    for char in '*:':
        quotes = quotes.replace(char, ' ')

    # remove linking pattern to other sources in {{}}
    pattern = r'\{\{[M|m]ain\|([\w ()\/\'\!\,\?\-\.]+)(?:#[\w \'\-]+)?\}\}'
    quotes = re.sub(pattern, '', quotes)

    # remove in-line comments
    quotes = re.sub(r'<!--[^<]+-->', ' ', quotes)

    # remove linking by extracting the actual words from [[]]
    link_pattern = r"\[\[([\w '\(\)\-,.\?\!#]+\|(?:\w+\|)?)?([\w\d ',.\-\?()\!]+)\]\]"
    links = re.findall(link_pattern, quotes)
    for link in links:
        rep = link[1]   # what to replace with
        if link[0] == '':
            original = '[[' + link[1] + ']]'
        else:
            original = '[[' + link[0] + link[1] + ']]'
        quotes = quotes.replace(original, rep)

    # go over line by line
    lines = ''
    for line in quotes.split('\n'):
        line = line.strip()

        # remove linking to images
        if '.jpg' in line.lower() or '.png' in line.lower():
            line = ''       

        # extract quote from a text with character name {{text|--|person|quote}}
        # |[e|E]mote|[b|B]ossemote
        text_quote = re.findall(r'\{\{(?:[t|T]ext)\|(?:[s|S]ay|[y|Y]ell|[w|W]hisper)\|([^|]+)\|([^\|\{]+)\}\}', line)
        if len(text_quote):
            character, line_1 = text_quote[0]

            # character can be a link
            charlink = re.findall(r'\{\{(npc|NPC)\|\|([\w \-\']+)(\|\|[\w \-\']+)?\}\}', character)
            if len(charlink):
                npc_, character, line_2 = charlink[0]
                line = line_1.replace(
                    '{{' + npc_ + '||' + character + line_2 + '}}',
                    line_2.replace('||', '')
                )
            
            # handle some nicknames
            character = nickname_map(character)

            # keep line if character is current character
            if not (character in charname or charname in character):
                line = ''
        else:
            charlink = re.findall(r'\{\{(npc|NPC)\|\|([\w \-\']+)(\|\|[\w \-\']+)?\}\}', line)
            if len(charlink):
                npc_, character, line_1 = charlink[0]
                line = line.replace(
                    '{{' + npc_ + '||' + character + line_1 + '}}',
                    line_1.replace('||', '')
                )

                # handle some nicknames
                character = nickname_map(character)

                # keep line if character is current character
                if not (character in charname or charname in character):
                    line = ''

        # extract quote from a text quote pattern {{text|--|quote}}
        # |[e|E]mote|[b|B]ossemote
        text_quote = re.findall(r'\{\{(?:text|Text)\|(?:[s|S]ay|[y|Y]ell|[w|W]hisper)\|(.+)\}\}', line)
        if len(text_quote):
            line = text_quote[0]
        
        # remove character quotes that are from a different character
        character = re.findall(r'\'\'\'([\w ]+)\'\'\'', line)
        if len(character):
            character = character[0]
            
            # handle some nicknames
            character = nickname_map(character)

            if character in charname or charname in character:
                line = re.sub(r'\'\'\'([\w ]+)\'\'\'', ' ', line)
            else:
                line = ''

        # extract text from gossip
        pattern_gossip = r"\{\{([G|g]ossip\|)(.+)\}\}"
        gossips = re.findall(pattern_gossip, line)
        if len(gossips):
            gossips = gossips[0]
            line = line.replace(
                '{{' + gossips[0] + gossips[1] + '}}',
                gossips[1]
            )
        
        # remove excess spaces
        line = line.strip()

        # remove references to unit quotes
        quote_headers = [
            '{{Novel-section|', '{{For|unit quotes|', 
            '{{Classic only-section', '{{Stub-section',
            '{{Seealso', '{{BC Classic only-section',
            '{{Col', '{{Comic-section', '{{Cleanup-section',
            '<!--', '{{rfb-section', '{{rfg-section', '{{seealso'
        ]
        for qh in quote_headers:
            if line.startswith(qh):
                line = ''

        # remove quote headers
        if (
            line.startswith("''For " + charname + "'s Warcraft") or
            line.startswith("''For " + charname.split(' ')[0] + "'s Warcraft") or 
            line.startswith(';') or 
            (line == 'When spoken to')
        ):
            line = ''

        # check again if any links were missing (nested)
        text_quote = re.findall(r'\{\{([^|{]+\|(?:[^|]+\|)?)(.+)\}\}', line)
        if len(text_quote):
            text_quote = text_quote[0]
            line = line.replace(
                '{{' + text_quote[0] + text_quote[1] + '}}',
                text_quote[1]
            )
        
        # remove 'actions'
        line = re.sub(r'<[\w .\/\',\?]+>', '', line)

        # remove ''+
        line = re.sub(r"''+", '', line)
        
        # finally remove {{}} and (), which after all other cleaning are NOT quotes.
        line = re.sub(r'\{\{[^\{\}]+\}\}', " ", line)
        line = re.sub(r'\([^\(\)]+\)', " ", line)

        # remove residue from not perfect regex
        line = re.sub(r'\w+=', ' ', line)

        # don't add empty lines
        if line:
            lines += line + '\n' 
    
    # finally remove specific characters
    for char in ['"', '“', '—', '[', ']']:
        lines = lines.replace(char, '')
    for char in [';']:
        lines = lines.replace(char, ' ')

    # remove excess spaces
    lines = re.sub(r'[ ]+', ' ', lines).strip()

    # save file
    with open(savepath, 'w', encoding='utf-8') as f:
        f.write(lines)
