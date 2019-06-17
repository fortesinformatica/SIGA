from src.utils.conn import *
import time


def mean_paths(paths):

    """

    :param paths: Modelos do problema 2
    :return: a media de caminhos por usuario, cnpj e produto
    """

    d = {
        "AC": {
            "user": 0,
            "cnpj": 0
        },
        "AG": {
            "user": 0,
            "cnpj": 0
        }
    }

    paths_user = [0, 0]
    paths_cnpj = [0, 0]
    # paths_product = [0, 0]
    for doc in paths:
        user = None if "user" not in doc else doc["user"]
        cnpj = None if "cnpj" not in doc else doc["cnpj"]
        product = None if "product" not in doc else doc["product"]

        if product == "AC":
            if user is not None:
                paths_user[0] += 1
                for size in doc["path_models"]["size"]:
                    d["AC"]["user"] += len(doc["path_models"]["size"][size])

            if user is None and cnpj is not None:
                paths_cnpj[0] += 1
                for size in doc["path_models"]["size"]:
                    d["AC"]["cnpj"] += len(doc["path_models"]["size"][size])

            """
            if flag_product:
                if user is None and cnpj is None:
                    paths_product[0] += 1
                    for size in doc["path_models"]["size"]:
                        d["AC"]["product"] += len(doc["path_models"]["size"][size])
            """
        elif product == "AG":
            if user is not None:
                paths_user[1] += 1
                for size in doc["path_models"]["size"]:
                    d["AG"]["user"] += len(doc["path_models"]["size"][size])

            if user is None and cnpj is not None:
                paths_cnpj[1] += 1
                for size in doc["path_models"]["size"]:
                    d["AG"]["cnpj"] += len(doc["path_models"]["size"][size])

            """
            if flag_product:
                if user is None and cnpj is None:
                    paths_product[1] += 1
                    for size in doc["path_models"]["size"]:
                        d["AG"]["product"] += len(doc["path_models"]["size"][size])
            """

    d["AC"]["user"] = int(d["AC"]["user"] / (1.0 * paths_user[0]))
    d["AC"]["cnpj"] = int(d["AC"]["cnpj"] / (1.0 * paths_cnpj[0]))

    d["AG"]["user"] = int(d["AG"]["user"] / (1.0 * paths_user[1]))
    d["AG"]["cnpj"] = int(d["AG"]["cnpj"] / (1.0 * paths_cnpj[1]))

    return d


if __name__ == '__main__':
    colleciton = get_collection('SigaPaths')
    total = colleciton.count()
    page = 1000
    print(total)

    cursor = colleciton.find(no_cursor_timeout=True).batch_size(100)
    paths = []
    product = []
    inicio = time.time()
    for d in range(page):
        try:
            doc = cursor.next()
            if doc['product'] == 'AC' or doc['product'] == 'AG':
                paths.append(doc)

        except Exception as e:
            print('Error', e)
            cursor.close()
    final = time.time()
    print('total time was:', final - inicio, 'in seconds')
    print("length documents:" + str(len(paths)))

    print("Calculating the mean of user, cnpj, product")
    """
        the format is the same of mean_(....)
    """
    mean_paths = mean_paths(paths)

    print("mean paths: ", mean_paths)
