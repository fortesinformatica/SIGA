import os
import sys
import bson

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

import numpy as np
from src.utils import blobs_service as service
from src.utils.log import Log

log = Log()


def reduce_model_counts(full_model, threshold=100000):
    """
    Reduz proporcionalmente a quantidade numerica de transições quando um transição atingir o limite superior

    :param full_model: modelo
    :param threshold: limite para a quantidade numerica máxima de transições
    :return:
    """

    model = full_model['model']
    for adj_list in model:
        if [True for transition in model[adj_list] if model[adj_list][transition] > threshold]:
            model[adj_list] = __reduce_counts__(model[adj_list])
    service.update(full_model, 'models')


def reduce_model_size(model, size_model, container='models'):
    """
    Reduz o tamanho em bytes do modelo

    :param model: modelo a ser reduzido
    :param size_model: tamanho atual do modelo
    :param container: container no Azure Storage
    :return:
    """

    max_size = int(os.getenv("MAX_MODEL_SIZE_IN_BYTES"))

    transition_lists = model['model']
    adjusted_list_size = {}
    transition_list_size = {}
    added = 0

    avg_frame_size = np.mean([len(bson.BSON.encode({k: ''})) for k in transition_lists.keys()])
    for k in transition_lists:
        transition_list_size[k] = len(bson.BSON.encode(transition_lists[k]))

    for k in transition_list_size:
        ls = transition_list_size[k]
        percent = ls/size_model
        new_list_length = round((percent * max_size) / avg_frame_size)

        if new_list_length < 5:
            added += avg_frame_size * (5 - new_list_length)

    for k in transition_list_size:
        ls = transition_list_size[k]
        percent = ls/(size_model + added)
        new_list_length = int(round((percent * max_size) / avg_frame_size))

        adjusted_list_size[k] = new_list_length if new_list_length > 4 else 5

    __adjust_transition_list__(model, adjusted_list_size, container)

    print(len(bson.BSON.encode(transition_lists)))

    return ""


def __adjust_transition_list__(model, adjusted_list_size, container='models'):
    transition_lists = model['model']
    for k in transition_lists:
        if len(transition_lists[k]) > 5:
            size_list = sorted(transition_lists[k].items(), key=lambda kv: kv[1])
            size_list.reverse()

            for sl in size_list[adjusted_list_size[k]:]:
                transition_lists[k].pop(sl[0])

    service.update(model, container)


def __reduce_counts__(adj_list):
    for transition in adj_list:
        adj_list[transition] = int(adj_list[transition] / 2)
        if adj_list[transition] < 1:
            adj_list.pop(transition)

    return adj_list
