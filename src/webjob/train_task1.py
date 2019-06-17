"""
TrainTask1
=====
Prover
    1. Leitura da base de dados contida no Azure Storage
    2. Treinamento dos modelos de Cadeias de Markov a partir dos dados lidos no Azure Storage
    3. Remove os dados já lidos na base de dados contida no Azure Storage

Como usar
    Adicione este script como um WebJob Continuous no Azure App Service "siga-api".
"""

import os
import sys
import json
import zlib

from datetime import datetime
from multiprocessing import Process


sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from src.utils.log import Log
from src.utils import blobs_service as service
from src.utils.storage.blobs import BlobManager
from src.tasks.task1.train_model import train_model
from src.webjob.check_database_size import write_on_file

log = Log()


def delete_documents(blobs):
    """
    Remove todos os blobs contidos na lista

    :param blobs: lista com os nomes dos blobs que serão removidos
    :return:
    """

    log.info("Deleting documents...")

    for blob in blobs:
        try:
            service.delete_entity(blob, 'timeline')
        except Exception as e:
            log.error('Error deleting blob {}: {}'.format(blob, e))

    log.info('Finished delete documents')


def train_user_sessions(user_session_data, blob_names):
    """
    Treina e remove os dados paralelamente utilizando multiprocessamento

    :param user_session_data: Dados das seções dos usuários que serão utilizados para o treinamento
    :param blob_names: lista dos blobs que serão removidos
    :return:
    """

    training = Process(target=train_model, args=[user_session_data])
    deleting = Process(target=delete_documents, args=[blob_names])

    try:
        training.start()
        deleting.start()

        training.join()
        deleting.join()
    except Exception as e:
        log.error(e)
        training.join()
        deleting.join()


def get_size_database():
    """
    Retorna a quantidade de blobs e tamanho da timeline em bytes.
    :return: int, int
    """
    try:
        with open(os.getenv("SIZE_DATABASE_FILE"), 'r') as content_file:
            timeline_sizes = content_file.readline().replace('\n', '').split('/')
    except Exception:
        log.warning("O Application Settings SIZE_DATABASE_FILE nao existe ou o webjob CheckDatabaseSize"
                    " nao esta funcionando")
        timeline_sizes = []

    if len(timeline_sizes) == 2 and timeline_sizes[0].isdigit() and timeline_sizes[1].isdigit():
        size_timeline_bytes = int(timeline_sizes[0])
        size_timeline_blobs = int(timeline_sizes[1])
    else:
        size_timeline_bytes = 1
        size_timeline_blobs = 1

    return size_timeline_blobs, size_timeline_bytes


def save_percent_trained_data(size_blobs, size_bytes):
    """
    Salva a quantidade de blobs e bytes lidos da timeline
    :param size_blobs: quantidade de blobs lidos
    :param size_bytes: quantidade de bytes lidos
    :return:
    """
    if size_blobs > sys.maxsize or size_bytes > sys.maxsize:
        log.warning("Representacao maxima recomendada para valores inteiros atingida. "
                    "Contagem do percentual treinado sera zerado")
        size_blobs = 0
        size_bytes = 0

    try:
        percent = "{}/{}\n".format(size_bytes, size_blobs)
        write_on_file(os.getenv("PERCENT_TRAINED"), percent)
    except Exception as e:
        log.error("Falha ao salvar porcentagem atual do treinamento. Application Settings PERCENT_TRAINED "
                  "nao configurado: {}".format(e))


def get_percent_trained():
    """
    Retorna a quantidade de de blobs e bytes ja lidos da timeline ou zero caso esses valores nao existam
    :return: int, int
    """
    try:
        with open(os.getenv("PERCENT_TRAINED"), 'r') as content_file:
            percent = content_file.readline().replace('\n', '').split('/')

        if len(percent) == 2 and percent[0].isdigit() and percent[1].isdigit():
            last_size_bytes = int(percent[0])
            last_size_blobs = int(percent[1])
        else:
            last_size_bytes = 0
            last_size_blobs = 0

    except Exception as e:
        log.error("Falha ao buscar porcentagem atual do treinamento. Application Settings PERCENT_TRAINED "
                  "nao configurado ou WebJob CheckDatabaseSize nao foi executado: {}".format(e))
        last_size_blobs = 0
        last_size_bytes = 0

    return last_size_blobs, last_size_bytes


if __name__ == '__main__':
    """
    Inicia o treinamento. Enquanto houver um next_maker, sera buscado no storage os proximos blobs.
    NUM_RESULT define a quantidade de blobs que serao listados por vez.
    
    O percentual de dados ja treinado e exibido nos arquivos de log. Todos os dias o tamanho da timeline e calculado e 
    atulizado.
    """

    NUM_RESULT = 600

    log.info('Started')
    today = datetime.today().day

    size_timeline_blobs, size_timeline_bytes = get_size_database()

    size_bytes = 0
    size_blobs = 0
    next_marker = None

    while next_marker != "":
        number_transitions = 0
        documents = []

        if size_bytes == 0 and size_blobs == 0:
            size_blobs, size_bytes = get_percent_trained()
            size_timeline_blobs += size_blobs
            size_timeline_bytes += size_bytes

        blob_names, next_marker = BlobManager.list_all_blobs(marker=next_marker, num_results=NUM_RESULT)
        size_blobs += len(blob_names)

        for blob_name in blob_names:
            try:
                blob_data = BlobManager.retrieve_zip_blob_with_document_name(blob_name)
            except Exception as e:
                log.error(e)
                continue

            if blob_data is None:
                continue

            size_bytes += sys.getsizeof(blob_data)

            final = zlib.decompress(blob_data, 16 + zlib.MAX_WBITS).decode('UTF-8')
            final_json = json.loads(final)
            documents.append(final_json)
            number_transitions += len(final_json)

        if len(documents) != 0:
            log.info('Training...')
            train_user_sessions(documents, blob_names)

            log.info('Trained {} transitions.'.format(number_transitions))
            log.info("Trained {} of {} blobs: {:.2f}%.".format(size_blobs, size_timeline_blobs,
                                                               size_blobs / size_timeline_blobs * 100))
            log.info("Trained {} of {} bytes: {:.2f}%.".format(size_bytes, size_timeline_bytes,
                                                               size_bytes / size_timeline_bytes * 100))

            log.info('Training Finished')

        if today != datetime.today().day:
            size_timeline_blobs, size_timeline_bytes = get_size_database()
            today = datetime.today().day

    save_percent_trained_data(size_blobs, size_bytes)
    log.info("Finished")
