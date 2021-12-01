import re
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
from glob import glob
import wikitextparser as wtp

import config


def fix_attr(attr):
    """ Takes the output of re.findall() as input and returns the 
        found attribute or 'Unknown' if the attribute was not found."""
    if attr:
        return attr[0]
    else:
        return 'Unknown'


if __name__ == "__main__":
    # get paths of all downloaded character files
    path_list = glob(config.PATH_CHARS + '*.txt')

    # get names of all downloaded characters
    name_list = [
        path.split('\\')[-1].replace('.txt', '').replace('_', ' ') 
        for path in path_list
    ]

    ## Create Graph with attributes
    G = nx.DiGraph()
    df = pd.DataFrame({'Name': name_list})
    for name, path in tqdm(zip(name_list, path_list), desc='Adding characters to graph'):
        # read text from downloaded character file 
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read()
        
        # get all fields from infobox
        txt_parsed = wtp.parse(txt).templates
        infobox = next(template for template in txt_parsed if 'Npcbox' in template.name.title())
        infobox_dict = dict([arg.name.strip(), arg.value.strip()] for arg in infobox.arguments)

        # get desired attributes from infobox
        race, gender, faction, status = 'Unknown', 'Unknown', 'Unknown', 'Unknown' 
        if 'race' in infobox_dict:
            race = re.sub(r'\s?<.*>', '', infobox_dict['race'])
        elif 'races' in infobox_dict:
            race = re.sub(r'\s?<.*>', '', infobox_dict['races'])
            if '[[' in race:
                race = re.findall(r'\[\[(.*?)(?:[\|#].*?)?\]\]', race)[0]
        if race != 'Unknown':
            race = race.title().replace('Dragon', 'Drake')
        
        if 'gender' in infobox_dict:
            gender = re.sub(r'\s?<.*>', '', infobox_dict['gender'])
        elif 'sex' in infobox_dict:
            gender = re.sub(r'\s?<.*>', '', infobox_dict['sex'])
        
        if 'faction' in infobox_dict:
            faction = re.sub(r'\s?<.*>', '', infobox_dict['faction'])

        if 'status' in infobox_dict:
            status = re.sub(r'\s?<.*>', '', infobox_dict['status'])
            status = re.sub(r'[,;]', '', status.split(' ')[0])

        # set other factions
        if faction not in ['Horde', 'Alliance']:
            faction = 'Neutral'
        

        # map status to Deceased/Alive
        if status in ['Killable', 'Active', 'Defunct', 'Defeatable', 'Imprisoned', 'Killable']:
            status = 'Alive'
        elif status in ['Deceased/Unknown', 'Sacrificed', 'Presumed', 'Reincarnating', 'Defeated']:
            status = 'Deceased'

        # add node with attributes
        G.add_node(
            name,
            gender=gender,
            race=race,
            faction=faction,
            status=status,
        )

        # add to DataFrame
        mask_ = df['Name'] == name
        df.loc[mask_, 'Gender'] = gender
        df.loc[mask_, 'Race'] = race
        df.loc[mask_, 'Faction'] = faction
        df.loc[mask_, 'Status'] = status

        # find all links on page
        links = np.unique(re.findall(r'\[\[(.*?)(?:[\|#].*?)?\]\]', txt))

        # add edges
        for link in links:
            if link in name_list:
                G.add_edge(name, link)

    # save Pandas DataFrame
    df.to_csv(config.PATH_RES + 'df_chars.csv', index=False)

    # create a new graph from the largest component in G
    Gcc = G.subgraph(max(nx.weakly_connected_components(G), key=len)).copy()

    # save graphs
    nx.write_gexf(G, config.PATH_RES + 'G_wow.gexf')
    nx.write_gexf(Gcc, config.PATH_RES + 'Gcc_wow.gexf')