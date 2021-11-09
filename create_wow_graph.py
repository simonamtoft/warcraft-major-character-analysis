import re
import numpy as np
import networkx as nx
from glob import glob


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

# Create Graph with attributes
G = nx.DiGraph()
for name, path in zip(name_list, path_list):
    # read text from downloaded character file 
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    
    # extract information about the character
    gender = fix_attr(re.findall(r'\| ?(?:gender|sex) ?= ?([\w]+)(?:<.+>)?\n', txt))
    race = fix_attr(re.findall(r'\| ?(?:race) ?= ?(.+)\n', txt))
    faction = fix_attr(re.findall(r'\| ?(?:faction) ?= ?(.+)\n', txt))
    status = fix_attr(re.findall(r'\| ?status *= ?(.+)\n', txt))
    # type_ = fix_attr(re.findall(r'\n\| ?(?:type) ?= ?(.+)\n', txt)) # wasn't that interesting
    # resource = fix_attr(re.findall(r'\| *(?:resource) *= *(.+)\n', txt)) # too many "Unknown"

    # take care of some specific race problems
    race = race.title().replace('Dragon', 'Drake')

    # remove comment about faction
    faction = faction.split('<')[0].strip()

    # remove space
    for char in '<,;({':
        status = status.split(char)[0]
    status = status.strip()

    # remove specifics from resource
    resource = resource.split('(')[0].strip()

    # add node with attributes
    G.add_node(
        name, gender=gender, 
        race=race, 
        faction=faction, 
        status=status, 
        # type=type_, 
        # resource=resource
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
