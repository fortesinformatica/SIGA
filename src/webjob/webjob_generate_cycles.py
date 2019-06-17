"""
GenerateCycles

A modification of networkx's implementation of Johnson's cycle finding algorithm
Original implementation: https://gist.github.com/qpwo/44b48595c2946bb8f823e2d72f687cd8
Original paper: Donald B Johnson. "Finding all the elementary circuits of a directed graph." SIAM Journal on Computing. 1975.

=====
Prover
    1. Gera os ciclos

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 0 * * 6

"""

import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from networkx import nx
from src.utils.storage.blobs import BlobManager, BlobsContainers
from src.utils.log import Log

log = Log()


def simple_cycles(G, threshold, limit=6):

    """

    :param G:  O grafo contendo todas as transições geradas a partir do modelo
    :param limit: Um valor máximo de caminho. Geralmente caminhos com valores maior que 10 tem uma probabilidade muito
    pequena e raramente são escolhidos
    :param threshold: Um valor mínimo de probabilidade para caminhos. Este parâmetro evita que caminhos muito longos,
    ou seja, com baixa probabilidade continuem a ser buscados, reduzindo assim o tempo de execução do algoritmo
    :return: Um dicionário com todas os ciclos de telas e suas respectivas probabilidades

    """

    subG = type(G)(G.edges())
    sccs = list(nx.strongly_connected_components(subG))
    while sccs:
        scc = sccs.pop()
        startnode = scc.pop()
        path = [startnode]
        blocked = set()
        blocked.add(startnode)
        stack = [(startnode, list(subG[startnode]))]

        stack_probability = 1

        while stack:

            thisnode, nbrs = stack[-1]

            if nbrs and len(path) < limit:
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                elif nextnode not in blocked:
                    edge_weigth = G.get_edge_data(thisnode, nextnode)['weight']

                    if stack_probability * edge_weigth > threshold:
                        stack_probability *= edge_weigth
                    else:
                        blocked.remove(thisnode)
                        stack.pop()
                        path.pop()
                        continue
                    path.append(nextnode)
                    stack.append((nextnode, list(subG[nextnode])))
                    blocked.add(nextnode)
                    continue
            if not nbrs or len(path) >= limit:
                blocked.remove(thisnode)
                stack.pop()
                path.pop()
        subG.remove_node(startnode)
        H = subG.subgraph(scc)
        sccs.extend(list(nx.strongly_connected_components(H)))

def strongly_connected_components(graph):

    """

    :param G:  O grafo contendo todas as transições geradas a partir do modelo
    :return: Um array de objetos do mesmo tipo de G com todas as componentes fortemente conectadas.

    """

    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []

    def _strong_connect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        successors = graph[node]
        for successor in successors:
            if successor not in index:
                _strong_connect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in stack:
                lowlink[node] = min(lowlink[node], index[successor])

        if lowlink[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node: break
            result.append(connected_component[:])

    for node in graph:
        if node not in index:
            _strong_connect(node)

    return result


def remove_node(G, target):
    """

    :param G:  O grafo contendo todas as transições geradas a partir do modelo
    :param target: vértices a ser removido do grafo
    :return: Um subgrafo do grafo G, removendo o vértice passado como parâmetro e todas as arestas que partem ou chegam
    nele

    """
    del G[target]
    for nbrs in G.values():
        nbrs.discard(target)


def subgraph(G, vertices):
    """

    :param G:  O grafo contendo todas as transições geradas a partir do modelo
    :param vertices: vértices que farão parte do novo grafo
    :return: Um subgrafo do grafo G, contendo apenas os vértices passados pelos parâmetro e as arestas que partem ou
    chegam nestes vértices

    """
    return {v: G[v] & vertices for v in vertices}



def cost_of_cycles(costs, cycles, threshold = 0.01):

    """

    :param costs: Array com os custos de cada ciclo
    :param cycles: Array com sequencias de telas
    :param threshold: Um valor mínimo de probabilidade para caminhos. Este parâmetro evita que caminhos muito longos,
    ou seja, com baixa probabilidade continuem a ser buscados, reduzindo assim o tempo de execução do algoritmo
    :return: Os caminhos ordenados por probabilidade.

    """

    cost_of_cycles = []
    new_cycles = []

    for cycle in cycles:
        cost = 1
        for i in range(0, len(cycle) - 1):
            current_cost = costs[cycle[i]][cycle[i + 1]]['weight']
            cost *= current_cost
        cost *= costs[cycle[len(cycle) - 1]][cycle[0]]['weight']
        if cost > threshold:
            cost_of_cycles.append(cost)
            new_cycle = cycle
            new_cycle.append(cycle[0])
            new_cycles.append(new_cycle)

    return [x for _, x in sorted(zip(cost_of_cycles, new_cycles), reverse=True)], sorted(cost_of_cycles, reverse=True)


def cycles(model, limit=6, threshold=0.01):

    """

    :param model:  O dicionário contendo informações de transições de telas para um conjunto de usuários.
    :param limit: Um valor máximo de caminho. Geralmente caminhos com valores maior que 10 tem uma probabilidade muito
    pequena e raramente são escolhidos
    :param threshold: Um valor mínimo de probabilidade para caminhos. Este parâmetro evita que caminhos muito longos,
    ou seja, com baixa probabilidade continuem a ser buscados, reduzindo assim o tempo de execução do algoritmo
    :return: Um novo model contendo as informações das telas dos caminhos gerados e seus respectivos custos

    """

    count_graph = model['model']

    probabilities_graph = {}

    for key in count_graph:
        transitions = count_graph[key]
        total = sum(transitions.values())
        features = {}
        for feature in transitions:
            features[feature] = {'weight': float(transitions[feature]) / total}
        probabilities_graph[key] = features

    graph = {}

    for key in list(probabilities_graph.keys()):
        graph[key] = list(probabilities_graph[key].keys())

    G = nx.DiGraph(probabilities_graph)

    all_simple_cycles = list(simple_cycles(G, limit=limit, threshold=threshold))

    all_cycles_sorted, cost_of_all_cycles = cost_of_cycles(probabilities_graph, all_simple_cycles, threshold=threshold)

    all_frames = []
    for cycle in all_cycles_sorted:
        all_frames += cycle

    all_frames = list(set(all_frames))

    model = []

    for i in range(len(all_cycles_sorted)):
        path = all_cycles_sorted[i]
        path_as_int = []

        for index in range(len(path)):
            path_as_int.append(all_frames.index(path[index]))
        model.append({"cost": cost_of_all_cycles[i], "path": path_as_int})

    return model, all_frames


marker = None

while True:

    models, new_marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, num_results=5, marker=marker)

    marker = new_marker

    total = len(models)

    for index, blob_name in enumerate(models):
        try:
            document = BlobManager.retrieve_blob_with_document_name(blob_name, container=BlobsContainers.models.value)
        except Exception as e:
            log.error(e)
            continue

        document = document[0]

        if index % 40 == 0:
            print(index * 100.0 / float(total))

        if 'model' not in document:
            continue
        model, frames = cycles(document, 6, threshold=0.05)
        data = {}
        # siga_paths.insert()
        data["model"] = model
        data["frames"] = frames
        data["product"] = document["product"]
        if 'cnpj' in document:
            data["cnpj"] = document["cnpj"]
            if 'user' in document:
                data["user"] = document["user"]
                data["model_id"] = document["product"] + document["cnpj"] + document["user"]
            else:
                data["model_id"] = document["product"] + document["cnpj"]
        else:
            data["model_id"] = document["product"]

        BlobManager.save_document_as_blob(data, container=BlobsContainers.cycles.value)

    if marker == '':
        break
