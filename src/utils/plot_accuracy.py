from src.utils.log import Log
from numpy import mean, arange
import time
import matplotlib.pyplot as plt
from src.utils.storage.blobs import BlobsContainers, BlobManager


def model_user(documents):
    count = 0
    mean_user_accuracy = list()  # lista das médias das acuracias dos modelos
    for docs in documents:
        user = None if "user" not in docs else docs["user"]
        if user is not None:
            best_accuracy_user = list()
            for accuracy in docs['accuracy']['historic']:
                if accuracy:
                    best_accuracy_user.append(max(accuracy))

            if best_accuracy_user:
                count += 1
                mean_user_accuracy.append(mean(best_accuracy_user))

    print(count)
    return mean_user_accuracy


def model_cnpj(documents):
    mean_cnpj_accuracy = list()
    count = 0
    for docs in documents:
        cnpj = None if "cnpj" not in docs else docs["cnpj"]
        user = None if "user" not in docs else docs["user"]
        if cnpj is not None and user is None:
            best_accuracy_cnpj = list()
            for accuracy in docs['accuracy']['historic']:
                if accuracy:
                    best_accuracy_cnpj.append(max(accuracy))

            if best_accuracy_cnpj:
                count += 1
                mean_cnpj_accuracy.append(mean(best_accuracy_cnpj))

    print(count)
    return mean_cnpj_accuracy


def model_product(documents):
    mean_product_accuracy = list()
    count = 0
    box_Ag = []
    box_Ac = []
    for docs in documents:
        user = None if "user" not in docs else docs["user"]
        product = None if "product" not in docs else docs["product"]
        if product == 'AG' and user is not None:
            best_accuracy_product = list()
            for accuracy in docs['accuracy']['historic']:
                if accuracy:
                    best_accuracy_product.append(max(accuracy))
            if best_accuracy_product:
                count += 1
                box_Ag.append(mean(best_accuracy_product))
        elif product == 'AC' and user is not None:
            best_accuracy_product = list()
            for accuracy in docs['accuracy']['historic']:
                if accuracy:
                    best_accuracy_product.append(max(accuracy))
            if best_accuracy_product:
                count += 1
                box_Ac.append(mean(best_accuracy_product))
    print(count)
    return box_Ag, box_Ac


def plot_model(Acuracies, user=False, cnpj=False, product=False):
    if product:
        Box_Ag = Acuracies[0]
        Box_Ac = Acuracies[1]
        plt.boxplot([Box_Ag, Box_Ac])
        plt.title('modelo de produto')
        plt.xticks([1, 2], ('AG', 'AC'))
        plt.yticks(arange(0, 1.1, 0.1))
        plt.show()
        return
    if user or cnpj:
        ranges = [[], [], [], [], [], [], [], [], [], []]
        for p in Acuracies:
            if 0.0 <= p < 0.1:
                ranges[0].append(p)
            elif 0.1 <= p < 0.2:
                ranges[1].append(p)
            elif 0.2 <= p < 0.3:
                ranges[2].append(p)
            elif 0.3 <= p < 0.4:
                ranges[3].append(p)
            elif 0.4 <= p < 0.5:
                ranges[4].append(p)
            elif 0.5 <= p < 0.6:
                ranges[5].append(p)
            elif 0.6 <= p < 0.7:
                ranges[6].append(p)
            elif 0.7 <= p < 0.8:
                ranges[7].append(p)
            elif 0.8 <= p < 0.9:
                ranges[8].append(p)
            elif p >= 0.9:
                ranges[9].append(p)

        lim_y = [ranges[0].__len__(), ranges[1].__len__(), ranges[2].__len__(), ranges[3].__len__(),
                 ranges[4].__len__(),
                 ranges[5].__len__(), ranges[6].__len__(), ranges[7].__len__(), ranges[8].__len__(),
                 ranges[9].__len__()]

        lim_x = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
        plt.bar(lim_x, lim_y, width=0.05)
        if user:
            plt.title('modelo de usuário')
        elif cnpj:
            plt.title('modelo de cnpj')

        plt.xticks(arange(0, 1.1, 0.1))
        plt.show()


log = Log()
if __name__ == '__main__':

    log.info("Started")
    initial_prefix = 'AC/'
    models, marker = BlobManager.list_all_blobs(container_name=BlobsContainers.models.value, num_results=1000,
                                                prefix=initial_prefix)
    documents = []

    begin = time.time()
    while True:
        next_marker = marker
        for index, blob_name in enumerate(models):
            try:
                doc = BlobManager.retrieve_blob_with_document_name(blob_name, container=BlobsContainers.models.value)[0]
                documents.append(doc)
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
    print("length documents:" + str(len(documents)))

    print('total time was:', end - begin, 'in seconds')

    Accuracy_user = model_user(documents)
    plot_model(Accuracy_user, user=True)
    Accuracy_cnpj = model_cnpj(documents)
    plot_model(Accuracy_cnpj, cnpj=True)
    Box_Ag, Box_Ac = model_product(documents)
    Accuracy_product = [Box_Ag, Box_Ac]
    plot_model(Accuracy_product, product=True)
