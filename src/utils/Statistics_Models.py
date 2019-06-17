from operator import itemgetter
from src.utils.storage.blobs import BlobManager, BlobsContainers
from src.utils.log import Log
import time


def count_frames(doc, Flag=False):
    """

    :param doc: Um dicionário contendo um modelo d problema 1
    :param Flag: Se True retorna uma lista com todas as telas daquele modelo, se False retorna o numero de telas
    daquele modelo.
    :return:  Se True retorna uma lista com todas as telas daquele modelo,
    se False retorna o numero de telas daquele modelo.
    """
    model = None if "model" not in doc else doc["model"]
    all_frames = list()
    if model is not None:
        frames_ext = [key for key in doc['model'].keys()]
        frames_int = [key_int for key in frames_ext for key_int in doc['model'][key].keys()]
        all_frames = list(set(frames_ext + frames_int))
    if Flag:
        return all_frames
    return all_frames.__len__()


def percent_model_frame(doc, all_frames):
    """

    :param doc:  Modelo
    :param all_frames: Todos as telas dos dois produtos
    :return: a porcentagem de quantas telas tem nesse modelo
    """

    frames = count_frames(doc, True)
    percent = 100 * (frames / 1.0 * all_frames)
    return percent


def rank(documents):
    """

    :param documents: Um dicionário contendo todos os modelos do problema 1
    :return: um rank das 10 telas mais acessadas, ou seja as 10 com maior probabilidade

    """
    rank = list()
    frames_frequence = total_frequence(documents)
    for i in range(10):
        rank.append(frames_frequence[i][0])

    return rank


def total_frequence(documents):
    """

    :param documents: Um dicionário contendo todos os modelos do problema 1
    :return: Um dicionário contendo a frequência de cada tela

    """
    dict_count = dict()
    for doc in documents:
        frames = count_frames(doc, True)
        for f in frames:
            if f not in dict_count.keys():
                dict_count.update({f: 1})
            elif f in dict_count.keys():
                dict_count[f] += 1
    total = sum([dict_count[key] for key in dict_count.keys()])
    dict_frequence = dict()
    for key, value in dict_count.items():
        dict_frequence.update({key: 100 * (value / (total * 1.0))})
    dict_frequence = sorted(dict_frequence.items(), key=itemgetter(1), reverse=True)
    return dict_frequence


def mean_(documents):
    """

    :param documents: Um dicionário contendo todos os modelos do problema 1
    :return: media de telas por usuario, cnpj e produto para os produtos AC e AG

    """
    d = {
        "AC": {
            "user": 0,
            "cnpj": 0,
            "product": 0
        },
        "AG": {
            "user": 0,
            "cnpj": 0,
            "product": 0
        }

    }

    total_user = [0, 0]
    total_cnpj = [0, 0]
    total_product = [0, 0]
    for doc in documents:
        user = None if "user" not in doc else doc["user"]
        cnpj = None if "cnpj" not in doc else doc["cnpj"]
        product = None if "product" not in doc else doc["product"]

        if product is "AC":
            if user is not None:
                total_user[0] += 1
                d["AC"]["user"] += count_frames(doc)

            if user is None and cnpj is not None:
                total_cnpj[0] += 1
                d["AC"]["cnpj"] += count_frames(doc)

            if user is None and cnpj is None:
                total_product[0] += 1
                d["AC"]["product"] += count_frames(doc)

        elif product is "AG":
            if user is not None:
                total_user[1] += 1
                d["AG"]["user"] += count_frames(doc)

            if user is None and cnpj is not None:
                total_cnpj[1] += 1
                d["AG"]["cnpj"] += count_frames(doc)

            if user is None and cnpj is None:
                total_product[1] += 1
                d["AG"]["product"] += count_frames(doc)

    d["AC"]["user"] = (d["AC"]["user"] / 1.0 * total_user[0])
    d["AC"]["cnpj"] = (d["AC"]["cnpj"] / 1.0 * total_cnpj[0])
    d["AC"]["product"] = (d["AC"]["product"] / 1.0 * total_product[0])

    d["AG"]["user"] = (d["AG"]["user"] / 1.0 * total_user[1])
    d["AG"]["cnpj"] = (d["AG"]["cnpj"] / 1.0 * total_cnpj[1])
    d["AG"]["product"] = (d["AG"]["product"] / 1.0 * total_product[1])

    return d


log = Log()
if __name__ == '__main__':

    log.info("Started")
    initial_prefix = 'AC/'
    models, marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, num_results=1000,
                                                prefix=initial_prefix)
    documents = []
    frames_AC = 0
    frames_AG = 0

    begin = time.time()
    while True:
        next_marker = marker
        for index, blob_name in enumerate(models):
            try:
                doc = BlobManager.retrieve_blob_with_document_name(blob_name, container=BlobsContainers.models.value)[0]
                documents.append(doc)
                cnpj = None if "cnpj" not in doc else doc["cnpj"]
                if cnpj is not None:
                    if doc["product"] == "AC":
                        frames_AC += 1
                    if doc["product"] == "AG":
                        frames_AG += 1
            except Exception as e:
                log.error(e)
                break
        if next_marker == '':
            if initial_prefix == 'AC/':
                initial_prefix = 'AG/'
            else:
                print('Finished')
                break
        models, marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, num_results=1000,
                                                    prefix=initial_prefix)
    end = time.time()

    print('total time was:', end - begin, 'in seconds')
    print("length documents:" + str(len(documents)))
    print("Total number of frames in AC: ", frames_AC.__len__())
    print("Total number of frames in AG: ", frames_AG.__len__())

    print('Calculating the frequency of each frame')
    """
        format is
        a = [(frame, frequence of the frame),....] in descending order
    """
    frequence = total_frequence(documents)
    print(frequence)
    print("Calculated: {} of {}".format(documents.__len__(), page))
    print("Calculating the mean of user, cnpj, product")

    mean_total = mean_(documents)
    print(mean_total)
    print(rank(documents))
