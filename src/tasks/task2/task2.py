import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from siga import next_frame
from operator import itemgetter

from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix, lil_matrix

cursor, frames = next_frame.get_data_by_user(1, 1, 1, 'mock2')

data, indexes = next_frame.train(cursor, frames)
idx = {val:key for (key, val) in indexes.items()}
#
# G = nx.from_numpy_array(data, create_using=nx.DiGraph())
# nx.draw(G, with_labels=True)
# plt.show()
# plt.savefig('graph.png')

transition = csr_matrix(data)

transition = -np.log(transition.multiply(1/transition.sum(axis=1)).toarray())

path_in_prob, predecessors = dijkstra(transition, return_predecessors=True)

def find(source, size=2):
    source = indexes[source]

    states_pred = list(set(predecessors[:, source]))

    states_pred.remove(-9999)
    cycles = []
    for state in states_pred:
        prob = path_in_prob[source, state] + path_in_prob[state, source]

        if prob == np.inf:
            return None
        path = __predecessors(source, state)
        path.reverse()
        path.append(source)
        cycles.append((prob, path))
    return sorted(cycles, key=itemgetter(0))

def __predecessors(source, first_predecessor):
    path = [first_predecessor]
    while path[-1] != source:
        path.append(predecessors[source, path[-1]])
    return path

cycles_in_frame = []
for frame in frames:
    cycles_in_frame.append({frame:find(frame)})

