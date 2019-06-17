"""
GeneratePaths

=====
Prover
    1. Gera os caminhos

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 0 * * 0

"""


import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from scipy.sparse.csgraph import dijkstra
from numpy import zeros, log, isnan, where, array, inf, exp
from operator import itemgetter
from src.utils.storage.blobs import BlobsContainers
from src.utils.storage.blobs import BlobManager


def normalization_models(matrix):
    """

    :param matrix:  Uma matriz i,j contendo o numero de vezes que o usuário mudou da tela i para a tela j
    :return: Uma matriz modificada de tal forma que possa utilizar-se o algoritmo de dijkstra, para achar os caminhos
    mais provaveis.

    """
    for frame_i in range(matrix.shape[0]):
        if sum(matrix[frame_i]) == matrix.shape[0] * matrix[frame_i][0]:
            matrix[frame_i] = 0.0
        for frame_j in range(matrix.shape[1]):
            if (matrix[frame_i][frame_j] == matrix[frame_i][frame_i]) and frame_i != frame_j:
                matrix[frame_i][frame_j] = 0.0

    matrix_normalized = (matrix.T / sum(matrix.T)).T
    return matrix_normalized


def transform_matrix(matrix):
    """

    :param matrix:  Uma matriz i,j contendo o numero de vezes que o usuário mudou da tela i para a tela j
    :return: Uma matriz modificada de tal forma que possa utilizar-se o algoritmo de dijkstra, para achar os caminhos
    mais provaveis.

    """
    matrix = normalization_models(matrix)
    for frame_i in range(matrix.shape[0]):
        for frame_j in range(matrix.shape[1]):
            if isnan(matrix[frame_i][frame_j]):
                matrix[frame_i][frame_j] = 0.0
            elif (matrix[frame_i][frame_j] != 0.0) and isnan(
                    matrix[frame_i][frame_j]):
                matrix[frame_i][frame_j] = -log(matrix[frame_i][frame_j])
    return matrix


def transform_data_to_matrix(model):
    """

    :param model: Um dicionário contendo todos os modelos do problema 1
    :return: Uma matriz i,j contendo o numero de vezes que o usuário mudou da tela i para a tela j


    """
    Frames = []
    for i_frame in model["model"]:
        Frames.append(i_frame)
        for j_frame in model["model"][i_frame]:
            if j_frame not in Frames:
                Frames.append(j_frame)
    Frames = array(Frames)
    N_frames = len(Frames)

    model_ = model["model"]
    matrix = zeros([N_frames, N_frames])
    for frame_i in range(len(Frames)):
        frame = Frames[frame_i]
        line = where(Frames == frame)[0][0]
        if frame in model_:
            for frames_j in model_[frame]:
                column = where(Frames == frames_j)[0][0]
                value = model_[frame][frames_j]
                matrix[line][column] = value

    return matrix, Frames.tolist()


def path(predecessors_, ind_, goal, prob):
    """

    Observação: Para utilizar-se esta função é necessario saber a tela de origem e a tela de destino.

    :param predecessors_: Matriz de predecessores contedo o caminho da tela inicial a tela final
    :param ind_: Tela de inicio
    :param goal: Tela Final
    :param prob: matriz de probabilidade contendo a probalidade do caminho da tela inicial a tela final
    :return: Caminho da tela inicial a tela final

    """
    min_array = predecessors_[ind_]
    path_way = [goal]
    i_initial = min_array[goal]
    while i_initial != ind_ and i_initial != -9999:
        path_way.append(i_initial)
        i_initial = min_array[i_initial]

    path_way.append(ind_)
    path_way.append(prob[ind_][goal])
    return path_way[::-1]


def path_size(predecessors_, size, prob):
    """

    Observação: Utilizado para descobrir caminhos de tamanho N

    :param predecessors_:  Matriz de predecessores contedo o caminho da tela inicial a tela final
    :param size: Tamnaho N
    :param prob: matriz de probabilidade contendo a probalidade do caminho da tela inicial a tela final
    :return: Todos os 5 melhores caminhos de tamanho N, ou  seja os 5 mais provaveis.

    """

    All_path_size = list()
    size = size + 1
    for ind_ in range(predecessors_.shape[1]):
        for goal in range(len(predecessors_[ind_])):
            if len(path(predecessors_, ind_, goal, prob)) == size and ind_ != goal:
                All_path_size.append(path(predecessors_, ind_, goal, prob))

    All_path_size = sorted(All_path_size, key=itemgetter(0))

    return All_path_size[:5]


def find_paths(matrix):
    """

    :param matrix: Uma matriz i,j contendo o numero de vezes que o usuário mudou da tela i para a tela j
    :return: Um dicionário contendo todos os caminhos de tamanho 2 a 10.

    """
    path_in_prob, predecessors = dijkstra(matrix, return_predecessors=True)
    size = 2
    paths = []
    while path_size(predecessors, size, path_in_prob) != []:
        paths.append(path_size(predecessors, size, path_in_prob))
        size += 1
        if size >= 10:
            break
    paths = sorted(paths, key=itemgetter(0))
    return paths


def save_sequences(paths_, user, cnpj, product, frames):
    """

    :param paths_: Um dicionário com os caminhos de um modelo
    :param user: Nome de usuario
    :param cnpj: Valor do Cnpj
    :param product: Nome do Produto
    :param frames: Todas as telas acessadas naquele modelo
    :return: Não existe retono, ele apenas salva na azure o modelo do problema dois, contendo nome de usuario, cnpj,
    produto, todos os caminhos daquele modelo e model_id.


    """
    path_models = list()
    frame = {}
    frame['user'] = user
    frame['product'] = product
    frame['cnpj'] = cnpj
    frame['frames'] = frames

    frame['model_id'] = frame['product']
    if frame['cnpj'] is not None:
        frame['model_id'] += frame['cnpj']
        if frame['user'] is not None:
            frame['model_id'] += frame['user']

    i = 1
    for size in range(len(paths_)):
        for path_i in paths_[size]:
            length = len(path_i)
            # path_models[i] = {"cost": path_i[0], "size": size, "path": array(path_i[1:length]).tolist()}
            if path_i[0] != inf:
                path_models.append({"cost": exp(-float(path_i[0])), "path": array(path_i[1:length]).tolist()})
        # path_models.append({"cost": float(path_i[0]), "size": size, "path": array(path_i[1:length]).tolist()})
        i += 1

    frame['model'] = path_models

    # json_data = dumps(frame)

    print("Saving in SigaPaths2 test")
    BlobManager.save_document_as_blob(frame, container=BlobsContainers.paths.value)
    print("Saved in SigaPaths2")


if __name__ == '__main__':
    models, marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, num_results=1000)

    while True:
        next_marker = marker
        for index, blob_name in enumerate(models):
            try:
                doc = BlobManager.retrieve_blob_with_document_name(blob_name)[0]

                user = None if "user" not in doc else doc["user"]
                cnpj = None if "cnpj" not in doc else doc["cnpj"]
                product = None if "product" not in doc else doc["product"]

                if 'model' in doc:
                    matrix_product, frames = transform_data_to_matrix(doc)
                    transition_matrix = transform_matrix(matrix_product)
                    paths = find_paths(transition_matrix)
                    save_sequences(paths, user, cnpj, product, frames)

            except Exception as e:
                print(e)
                continue

        models, marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, marker=next_marker,
                                                    num_results=1000)
        if next_marker == '':
            print('Finished')
            break
