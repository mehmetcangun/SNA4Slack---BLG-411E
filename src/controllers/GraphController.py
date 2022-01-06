import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.bridges import bridges
from networkx.algorithms.centrality.degree_alg import degree_centrality
from networkx.algorithms.approximation import all_pairs_node_connectivity
import glob
from networkx.classes.function import subgraph
from networkx.drawing import layout
import os
from flask import current_app as app
from numpy.lib.function_base import extract


userlist_id_name_dict = {}
channel_names = []

def add_channel_to_graph(channel, G):
    for item in channel:
        if item.get('reply_users'):
            thread_owner = item['user']
            for i in item['reply_users']:
                if thread_owner != i:
                    if G.has_edge(i,thread_owner):
                        G[i][thread_owner]['weight'] += 1
                        print(G[i][thread_owner]['weight'])
                    else:
                        G.add_edge(i,thread_owner, weight= 1)


def metric_calc(Graph, metric_id, userlist_id_name_dict):
    result = {}
    if(metric_id == 0):
        degree = degree_centrality(Graph)
        list_degree = degree.items()
        for nodes in list_degree:
            name = userlist_id_name_dict[nodes[0]]
            result[name] = nodes[1]
    elif(metric_id == 1):
        result = []
        list_bridges = list(bridges(Graph))
        for node in list_bridges:
            edge = (userlist_id_name_dict[node[0]],userlist_id_name_dict[node[1]])
            result.append(edge)
    elif(metric_id == 2):
        result = all_pairs_node_connectivity(Graph)
    return result


def layout_for_graph(Graph, layout_id):
    if(layout_id == 0):
        top = nx.bipartite.sets(Graph)[0]
        pos = nx.bipartite_layout(Graph, top)
    elif(layout_id == 1):
        pos = nx.circular_layout(Graph)
    elif(layout_id == 2):
        pos = nx.planar_layout(Graph)
    elif(layout_id == 3):
        pos = nx.spiral_layout(Graph)
    return pos



def draw_graph(graph, layout_id):
    pos = layout_for_graph(graph,layout_id)
    nx.draw_networkx(graph,pos,with_labels=False)
    nx.draw_networkx_labels(graph,pos,userlist_id_name_dict)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)

def run_graph(metric_id, layout_id, foldername):
    G,subgraphs = read_all(foldername)
    General_graph = draw_graph(G, layout_id)
    general_metric = metric_calc(G, metric_id)
    subgraphs_drawed = []
    for index, graph in enumerate(subgraphs):
        draw_graph(graph, layout_id)
        graph_name = channel_names[index] + ".png"
        path = os.path.join(app.config['UPLOAD_FOLDER'], foldername, graph_name) # folderın içine mi çıkacak?
        plt.savefig(path, format="PNG")
        
    """ return format: channel array with name, img """
    return [
        { "name": "graph", "img": "static/uploads/graph.png"},
        { "name": "hey", "img": "static/uploads/hey.png"},
        { "name": "general", "img": "static/uploads/general.png"},
    ]

def read_all(foldername):
    G = nx.Graph()
    S = nx.Graph()

    userlist_f = open('users.json')
    userlist_p = json.load(userlist_f)

    channellist_f = open('channels.json')
    channellist_p = json.load(channellist_f)

    #channel listten kanalları çekip hepsinde çalışacak:


    for i in channellist_p:
        name = i['name']
        channel_names.append(name)

    extract_path = os.path.join(app.config['UPLOAD_FOLDER'], foldername, "extract")
    json_files = []
    for i in channel_names:
        x = glob.glob('{path}/{0}/*.json'.format(extract_path, i))
        json_files.append(x)


    for i in userlist_p:
        i_id = i['id']
        i_name = i['name']
        userlist_id_name_dict[i_id] = i_name
        G.add_node(i_id)
        S.add_node(i_id)


    subgraphs = []
    for files in json_files:
        subgraph = S
        for file in files:
            messagelist_f = open(file)
            messagelist_p = json.load(messagelist_f)
            add_channel_to_graph(messagelist_p, G)
            add_channel_to_graph(messagelist_p,subgraph)
        subgraphs.append(subgraph)
    return G,subgraphs

#plt.show()
