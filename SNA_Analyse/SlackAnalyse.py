import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.centrality.degree_alg import degree_centrality
import glob
import os


G = nx.Graph()


userlist_f = open('users.json')
userlist_p = json.load(userlist_f)


channellist_f = open('channels.json')
channellist_p = json.load(channellist_f)

#channel listten kanalları çekip hepsinde çalışacak:

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


userlist_id_name_dict = {}
channel_names = []

for i in channellist_p:
    name = i['name']
    channel_names.append(name)

json_files = []
for i in channel_names:
    x = glob.glob('{0}/*.json'.format(i))
    json_files.append(x[0])

#for in json file def iterete - open firts


for i in userlist_p:
    i_id = i['id']
    i_name = i['name']
    userlist_id_name_dict[i_id] = i_name
    G.add_node(i_id)


for file in json_files:
    messagelist_f = open(file)
    messagelist_p = json.load(messagelist_f)
    add_channel_to_graph(messagelist_p, G)

top = nx.bipartite.sets(G)[0]
pos = nx.bipartite_layout(G, top)
nx.draw_networkx(G,pos,with_labels=False)

nx.draw_networkx_labels(G,pos,userlist_id_name_dict)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.savefig("Graph.png", format="PNG")
plt.show()