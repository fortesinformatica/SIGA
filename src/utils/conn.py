import numpy as np

from urllib.parse import unquote
from werkzeug.exceptions import Unauthorized
from src.utils.exceptions import *
from src.utils.storage.blobs import *
from src.utils import blobs_service as service


def authenticate_request(authorization):

    if (authorization is None or getenv("AUTH_USER") != authorization.username
            or getenv("AUTH_PASS") != authorization.password):
        raise Unauthorized()


def get_model(user_id=None, cnpj_id=None, prod_id=None):

    user_id = unquote(unquote(user_id))
    cnpj_id = unquote(unquote(cnpj_id))
    prod_id = unquote(unquote(prod_id))

    user_model = service.find_one(product=prod_id, cnpj=cnpj_id, user=user_id)
    cnpj_model = service.find_one(product=prod_id, cnpj=cnpj_id, user=None)
    prod_model = service.find_one(product=prod_id, cnpj=None, user=None)

    model = __select_best_model__(user_model, cnpj_model, prod_model)

    if model is None:
        raise NotFound('Recurso inexistente')

    formatted_model = format_model_output(model)

    if user_id is not None:
        formatted_model["user"] = user_id
    if cnpj_id is not None:
        formatted_model["cnpj"] = cnpj_id

    return formatted_model


def get_storage_model(user_id=None, cnpj_id=None, prod_id=None, container = BlobsContainers.models.value):

    blob_model = BlobManager.retrieve_blob_with_document_data(user=user_id, cnpj=cnpj_id, product=prod_id, container=container)
    if blob_model is not None:
        return blob_model
    else:
        raise NotFound()


def format_model_output(sample):

    frames_ext = [key for key in sample['model'].keys()]
    frames_int = [key_int for key in frames_ext for key_int in sample['model'][key].keys()]
    all_frames = list(set(frames_ext + frames_int))
    other_keys = ["_id", "id", "accuracy"]

    for key in other_keys:
        sample.pop(key, None)

    models = sample["model"]
    recommendations = sample
    recommendations["frames"] = all_frames
    recommendations["model"] = {}

    for frame in frames_ext:
        values = list(models[frame].keys())
        indexes = [all_frames.index(value) for value in values]
        recommendations["model"][frame] = list(reversed(indexes))

    return recommendations


def __select_best_model__(user_model, cnpj_model, prod_model):

    accuracy_user = 0
    accuracy_cnpj = 0
    accuracy_prod = 0

    if user_model is not None:
        accuracy_user = __get_hits__(user_model)
    if cnpj_model is not None:
        accuracy_cnpj = __get_hits__(cnpj_model)
    if prod_model is not None:
        accuracy_prod = __get_hits__(prod_model)

    if accuracy_prod < accuracy_user > accuracy_cnpj:
        return user_model
    elif accuracy_cnpj > accuracy_prod:
        return cnpj_model
    else:
        return prod_model


def __get_hits__(model):

    hist = model['accuracy']['historic']
    if hist.count([]) != 0:
        hist.remove([])

    hits = np.array(hist)
    return np.mean(hits[:, -1:]) if (len(hits) != 0) else 0

