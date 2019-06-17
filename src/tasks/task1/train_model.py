import datetime

from src.ml.models.markov import markov_chain
from copy import deepcopy as copy
from src.utils import blobs_service as service
from src.utils.log import Log
from operator import itemgetter


log_app = Log()


def train_model(user_sessions_data):
    """
    Utiliza cada sequência de telas de uma seção de um usuário  por vez para treinar os modelos

    :param user_sessions_data: Dados contendo as sequências de telas das seções dos usuários
    :return:
    """

    for user_data in user_sessions_data:
        data = get_activate_data(user_data)
        if data:
            train_product(data)


def train_product(product_data):
    """
    Treina o modelo do produto a partir do modelo atualizado do usuário

    :param product_data: sequências de telas de uma seção de um usuários
    :return:
    """

    product = product_data[0]['product']

    product_model = service.find_one(product)

    train_data = dict()
    train_data['product'] = product
    train_data['model'] = {}
    train_data['accuracy'] = {'day': datetime.datetime.strptime(product_data[0]['time'], '%Y-%m-%dT%H:%M:%S').day,
                              'total': 0,
                              'hits': [],
                              'historic': []}

    if product_model and len(product_data) != 0:
        if 'accuracy' not in product_model:
            product_model['accuracy'] = train_data['accuracy']

        train_data = __update_model__(product_data, product_model, train_data)

    model_cnpj = train_cnpj(product_data)
    train_data['model'] = sum_models(train_data['model'], model_cnpj)

    service.update(train_data, 'models')


def train_cnpj(cnpj_data):
    """
    Treina o modelo do CNPJ a partir do modelo atualizado do usuário

    :param cnpj_data: sequências de telas de uma seção de um usuários
    :return: modelo do usuário treinado
    """

    product = cnpj_data[0]['product']
    cnpj = cnpj_data[0]['cnpj']

    cnpj_model = service.find_one(product, cnpj=cnpj)

    train_data = dict()
    train_data['product'] = product
    train_data['cnpj'] = cnpj
    train_data['model'] = {}
    train_data['accuracy'] = {'day': datetime.datetime.strptime(cnpj_data[0]['time'], '%Y-%m-%dT%H:%M:%S').day,
                              'total': 0,
                              'hits': [],
                              'historic': []}

    if cnpj_model and len(cnpj_data) != 0:
        if 'accuracy' not in cnpj_model:
            cnpj_model['accuracy'] = train_data['accuracy']

        train_data = __update_model__(cnpj_data, cnpj_model, train_data)

    model_user = train_user(cnpj_data)

    train_data['model'] = sum_models(train_data['model'], model_user)
    service.update(train_data, 'models')

    return model_user


def train_user(user_data):
    """
    Treina o modelo do usuário a partir das sequências

    :param user_data: sequências de telas de uma seção de um usuários
    :return: modelo do usuário treinado
    """

    product = user_data[0]['product']
    cnpj = user_data[0]['cnpj']
    user = user_data[0]['user']

    user_model = service.find_one(product, cnpj, user)
    trained_model_now = markov_chain.train(user_data)

    train_data = dict()
    train_data['product'] = product
    train_data['cnpj'] = cnpj
    train_data['user'] = user
    train_data['model'] = copy(trained_model_now)
    train_data['accuracy'] = {'day': datetime.datetime.strptime(user_data[0]['time'], '%Y-%m-%dT%H:%M:%S').day,
                              'total': 0,
                              'hits': [],
                              'historic': []}

    if user_model is not None and len(user_data) != 0:
        if 'accuracy' not in user_model:
            user_model['accuracy'] = train_data['accuracy']

        train_data = __update_model__(user_data, user_model, train_data)

    service.update(train_data, 'models')

    return trained_model_now


def sum_models(model, actual):
    """
    Soma dois modelos

    :param model:
    :param actual:
    :return: um modelo atualizado com as somas dos modelos passados como pârametros
    """

    model = copy(model)
    actual = copy(actual)

    updated_model = copy(actual)
    for feature in model:
        if feature in actual.keys():
            for adj_feature in model[feature].keys():
                if adj_feature in actual[feature].keys():
                    updated_model[feature][adj_feature] = \
                        model[feature][adj_feature] + actual[feature][
                            adj_feature]
                else:
                    updated_model[feature][adj_feature] = model[feature][
                        adj_feature]
        else:
            updated_model[feature] = model[feature]
    return updated_model


def get_activate_data(data):
    """
    Retorna uma lista contendo apenas os daos que contem o "rowType" marcado como "Activate"

    :param data: sequências completa
    :return: sequência apenas com os dados marcados como "Activate"
    """

    filtered_data = [item for item in data if item['rowType'] == 'Activate']
    filtered_data = sorted(filtered_data, key=itemgetter('instanceId', 'time'))
    activate_data = []

    previous_feature = None
    for d in filtered_data:
        if d['feature'] != previous_feature:
            activate_data.append(d)

        previous_feature = d['feature']
    return activate_data


def __update_model__(data, model, train_data):
    """
    Atualiza o modelo atual em relação ao recem treinado

    :param data: dados que serão utilizados para calcular a acurácia do modelo atual
    :param model: modelo atual
    :param train_data: modelo recém treinado
    :return:
    """

    if 'model' not in model:
        return train_data

    acc_user = markov_chain.accuracy(data, model['model'])
    train_data['model'] = sum_models(train_data['model'], model['model'])

    acc_user = [round(x, 2) for x in acc_user]

    if model['accuracy']['day'] != train_data['accuracy']['day']:
        acc = model['accuracy']['hits']

        model['accuracy']['historic'].append(acc)
        train_data['accuracy']['historic'] = model['accuracy']['historic']

        if len(train_data['accuracy']['historic']) > 30:
            train_data['accuracy']['historic'].pop(0)
    else:
        train_data['accuracy'] = model['accuracy']

    if len(train_data['accuracy']['hits']) == 0:
        train_data['accuracy']['hits'] = acc_user
    else:
        new_total = len(data) + train_data['accuracy']['total']
        for i in range(len(acc_user)):
            new_acc_user = acc_user[i] * len(data) / new_total
            train_data['accuracy']['hits'][i] *= train_data['accuracy']['total']
            train_data['accuracy']['hits'][i] /= new_total
            train_data['accuracy']['hits'][i] += new_acc_user
            train_data['accuracy']['hits'][i] = round(train_data['accuracy']['hits'][i], 2)

    train_data['accuracy']['total'] += len(data)

    return train_data
