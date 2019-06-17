"""
CheckDatabaseSize
=====
Prover
    1. Calculo da tamanho da timeline em quantidade de blobs e em bytes
    2. Salva as informações de tamanho da timeline nos arquivos definidos pelas Application Settings

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 2 * * *
"""

import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from src.utils.storage.blobs import BlobManager
from src.utils.log import Log

log = Log()


def write_on_file(filename, lines, mode='w'):
    with open(filename, mode) as content_file:
        content_file.writelines(lines)


def historic_database_size(str_sizes):
    """
    Mantem o historico do tamanho da base de dados em bytes e em quantidade de blobs dos ultimos 30 dias.

    :param str_sizes:
    :return:
    """
    number_of_days = 31

    try:
        historic_file = os.getenv("HISTORIC_DATABASE_SIZE")
    except Exception as e:
        log.error("Application Settings HISTORIC_DATABASE_SIZE nao definido: {}".format(e))
        return

    if not os.path.exists(historic_file):
        write_on_file(historic_file, str_sizes)

    else:
        with open(historic_file, 'r') as content_file:
            str_size_timeline = content_file.readlines()

        if len(str_size_timeline) >= number_of_days:
            str_size_timeline.pop(0)
            str_size_timeline.append(str_sizes)

            write_on_file(historic_file, str_size_timeline)
        else:
            write_on_file(historic_file, str_sizes, mode='a')


if __name__ == '__main__':
    size_timeline_bytes, size_timeline_blobs = BlobManager.get_container_size('timeline')

    str_sizes = "{}/{}\n".format(size_timeline_bytes, size_timeline_blobs)
    try:
        write_on_file(os.getenv('SIZE_DATABASE_FILE'), str_sizes, 'w')
    except Exception as e:
        log.error("Application Settings SIZE_DATABASE_FILE nao definido: {}".format(e))

    historic_database_size(str_sizes)
