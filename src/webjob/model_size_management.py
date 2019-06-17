"""
ModelSizeManagement
=====
Prover
    1. Gerenciamento do tamanho máximo de cada modelo contido container Models no Azure Storage
    2. Limite máximo numerico da quantidade de transições em cada modelo contido container Models no Azure Storage
    3. Ajusta todos os modelos que estiverem fora das especificações

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 0 */15 * *
"""


import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from src.utils.storage.blobs import BlobManager
from src.utils.model_management import reduce_model_size, reduce_model_counts
from src.utils.log import Log

log = Log()
max_size = int(os.getenv("MAX_MODEL_SIZE_IN_BYTES"))
next_marker = None

while True:
    blob_names, marker = BlobManager.list_all_blobs(marker=next_marker, num_results=1000, container_name='model')
    next_marker = marker

    for b_name in blob_names:
        try:
            m, blob = BlobManager.retrieve_blob_with_document_name(b_name, 'model')
            size_model = len(blob.content.decode('utf-8'))
            if size_model > max_size:
                reduce_model_size(m, size_model)
                reduce_model_counts(m)
        except Exception as e:
            log.error(e)
            exit(1)

    if next_marker == "":
        break
