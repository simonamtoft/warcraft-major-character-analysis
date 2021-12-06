import numpy as np
import networkx as nx


def get_mode(x):
    """Gets the mode value of a numpy array (most frequently occurring value)"""
    vals, counts = np.unique(x, return_counts=True)
    return vals[np.argmax(counts)]


def get_degree_stats(title, deg):
    """Return string of min, max, mean, median and mode of numpy array with a title"""
    return f'{title}\t{deg.min()}\t{deg.max()}\t{deg.mean():.2f}\t{np.median(deg)}\t{get_mode(deg)}'


def get_degs(G):
    in_deg = np.array([d for _, d in G.in_degree()])
    out_deg = np.array([d for _, d in G.out_degree()])
    tot_deg = np.array([d for _, d in G.degree()])
    return in_deg, out_deg, tot_deg


def html_all_degree_stats(G, save_path):
    """Save degree stats for in-, out- and total-degree of the networkx graph G to a HTML table."""
    in_deg, out_deg, tot_deg = get_degs(G)

    table = "<table>\n"
    
    # create header
    table += "  <tr>\n"
    for col in ['min', 'max', 'mean', 'median', 'mode']:
        table += "    <th>{0}</th>\n".format(col)
    table += "  </tr>\n"

    # add row data
    for line in [
        get_degree_stats("In-degree", in_deg),
        get_degree_stats("Out-degree", out_deg),
        get_degree_stats("Total-degree", tot_deg)
    ]:
        row = line.split('\t')
        table += "  <tr>\n"
        for col in row:
            table += "    <td>{0}</td>\n".format(col.strip())
        table += "  </tr>\n"

    # finalize
    table += "</table>"

    # save html to text file
    with open(save_path, 'w') as f:
        f.write(table)


def print_all_degree_stats(G):
    """Print degree stats for in-, out- and total-degrees of the networkx graph G"""
    in_deg, out_deg, tot_deg = get_degs(G)

    print('\t\tmin\tmax\tmean\tmedian\tmode')
    print(get_degree_stats("In-degree", in_deg))
    print(get_degree_stats("Out-degree", out_deg))
    print(get_degree_stats("Total-degree", tot_deg))


def get_centrality_measure(G, centrality_name):
    """Compute the centrality measure of networkx graph G"""
    if centrality_name == 'deg':
        return nx.degree_centrality(G).items()
    elif centrality_name == 'bwn':
        return nx.betweenness_centrality(G).items()
    elif centrality_name == 'eig':
        return nx.eigenvector_centrality(G).items()


def compute_centrality_faction(G, centrality_name):
    # compute the specified centrality measure
    centrality_measure = get_centrality_measure(G, centrality_name)

    # split centrality
    horde_centrality = []
    alliance_centrality = []
    neutral_centrality = []
    for k, v in centrality_measure:
        if G.nodes(data=True)[k]['faction'] == 'Horde':
            horde_centrality.append(v)
        elif G.nodes(data=True)[k]['faction'] == 'Alliance':
            alliance_centrality.append(v)
        else:
            neutral_centrality.append(v)
    
    # return the mean of specified centrality measure for horde, alliance and neutral
    return (
        np.array(horde_centrality).mean(), 
        np.array(alliance_centrality).mean(), 
        np.array(neutral_centrality).mean()
    )


def compute_centrality_gender(G, centrality_name):
    # compute the specified centrality measure
    centrality_measure = get_centrality_measure(G, centrality_name)

    # split centrality
    male_centrality = []
    female_centrality = []
    for k, v in centrality_measure:
        if G.nodes(data=True)[k]['gender'] == 'Male':
            male_centrality.append(v)
        else:
            female_centrality.append(v)
    
    # return the mean of specified centrality measure for male and female
    return (
        np.array(male_centrality).mean(), 
        np.array(female_centrality).mean()
    )


def compute_centrality_status(G, centrality_name):
    # compute the specified centrality measure
    centrality_measure = get_centrality_measure(G, centrality_name)

    # split centrality
    alive_centrality = []
    deceased_centrality = []
    for k, v in centrality_measure:
        if G.nodes(data=True)[k]['status'] == 'Alive':
            alive_centrality.append(v)
        else:
            deceased_centrality.append(v)
    
    # return the mean of specified centrality measure for alive and deceased
    return (
        np.array(alive_centrality).mean(), 
        np.array(deceased_centrality).mean()
    )


def html_centralities(save_path, columns, row_data):
    """Save degree stats for in-, out- and total-degree of the networkx graph G to a HTML table."""
    table = "<table>\n"
    
    # create header
    table += "  <tr>\n"
    for col in columns:
        table += "    <th>{0}</th>\n".format(col)
    table += "  </tr>\n"

    # add row data
    for line in row_data:
        row = line.split('\t')
        table += "  <tr>\n"
        for col in row:
            table += "    <td>{0}</td>\n".format(col.strip())
        table += "  </tr>\n"

    # finalize
    table += "</table>"

    # save html to text file
    with open(save_path, 'w') as f:
        f.write(table)


def get_nodes_from_attr(G, attr_name, attr):
    return [node[0] for node in G.nodes(data=True) if node[1][attr_name] == attr]
