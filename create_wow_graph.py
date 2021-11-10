import re
import numpy as np
import networkx as nx
from glob import glob
import wikitextparser as wtp


def fix_attr(attr):
    """ Takes the output of re.findall() as input and returns the 
        found attribute or 'Unknown' if the attribute was not found."""
    if attr:
        return attr[0]
    else:
        return 'Unknown'


# get paths of all downloaded character files
path_list = glob('./data/wow_chars/*.txt')

# get names of all downloaded characters
name_list = [
    path.split('\\')[-1].replace('.txt', '').replace('_', ' ') 
    for path in path_list
]

## Create Graph with attributes
G = nx.DiGraph()
for name, path in zip(name_list, path_list):
    # read text from downloaded character file 
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    
    # get all fields from infobox
    txt_parsed = wtp.parse(txt).templates
    infobox = next(template for template in txt_parsed if 'Npcbox' in template.name.title())
    infobox_dict = dict([arg.name.strip(), arg.value.strip()] for arg in infobox.arguments)


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

    # add node with attributes
    G.add_node(
        name, 
        gender=gender, 
        race=race, 
        faction=faction, 
        status=status,
    )

    # find all links on page
    links = np.unique(re.findall(r'\[\[(.*?)(?:[\|#].*?)?\]\]', txt))

    # add edges
    for link in links:
        if link in name_list:
            G.add_edge(name, link)

# create a new graph from the largest component in G
Gcc = G.subgraph(max(nx.weakly_connected_components(G), key=len)).copy()

# save graphs
nx.write_gexf(G, './saved_graphs/G_wow.gexf')
nx.write_gexf(Gcc, './saved_graphs/Gcc_wow.gexf')