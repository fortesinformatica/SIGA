def train(data):
    """
    Treina o modelo da Cadeia de Markov a partir

    :param data: dados utilizados para treinamento
    :return: modelo treinado
    """
    model = {}
    item_before = None

    for item_actual in data:

        if item_before:
            __count__(item_before, item_actual, model)
            item_before = item_actual
        else:
            item_before = item_actual

    return model


def __count__(item_before, item_actual, model):
    """
    Cacula e atuliza cada transição na matriz de transições da Cadeia de Markov

    :param item_before:
    :param item_actual:
    :param model:
    :return:
    """

    if item_before['feature'] in model.keys():
        if item_actual['feature'] in model[item_before['feature']]:
            model[item_before['feature']][item_actual['feature']] += 1
        else:
            model[item_before['feature']][item_actual['feature']] = 1
    else:
        model[item_before['feature']] = {}
        model[item_before['feature']][item_actual['feature']] = 1


def predict(model, feature, size_rank=5):
    """
    Prediz a próxima tela

    :param model: modelo
    :param feature: tela atual
    :param size_rank: quantidade de sugestões a serem consideradas
    :return: uma lista com todas as possíveis telas na ordem de maior probailidade para menor probabilidade
    """

    if feature in model:
        adj_features = model[feature]
    else:
        return []

    rank = sorted(adj_features.items(), key=lambda x: x[1], reverse=True)
    rank = [k for k, v in rank]

    return rank[0:size_rank]


def accuracy(test_data, model, rank=5):
    """
    Calcula a acurácia de um modelo

    :param test_data: Dados utilizados para teste
    :param model: modelo a ser calculado a acurácia
    :param rank:  quantidade de sugestões a serem consideradas
    :return: uma lista com a acurácia para cada rank
    """

    result = []
    for rank_size in range(1, rank+1):
        count = 0
        ignore = 0

        rank = predict(model, test_data[0]['feature'], rank_size)
        last_feature = test_data[0]['feature']
        last_instanceid = test_data[0]['instanceId']

        for i in range(1, len(test_data)):
            if test_data[i]['feature'] == last_feature:
                ignore += 1
                continue

            if test_data[i]['instanceId'] != last_instanceid:
                ignore += 1
            elif test_data[i]['feature'] in rank:
                count += 1

            rank = predict(model, test_data[i]['feature'], rank_size)
            last_feature = test_data[i]['feature']
            last_instanceid = test_data[i]['instanceId']

        rate = count / (len(test_data) - ignore)
        result.append(rate)

    return result
