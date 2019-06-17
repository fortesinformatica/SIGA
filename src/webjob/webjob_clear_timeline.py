"""
ClearTimeLine
=====
Prover
    1. Procura blobs fora padrão definido e os apaga

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 */3 * * *
"""

import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

from src.utils.storage.blobs import BlobManager
from src.utils.storage.blobs import BlobsContainers

if __name__ == '__main__':

    next_marker = ''

    while True:

        timeline = BlobManager.block_blob_service.list_blobs(container_name=BlobsContainers.timeline.value,
                                                             num_results=1000
                                                             , prefix=None, marker=next_marker)
        next_marker = timeline.next_marker
        delete = 0
        for blob in timeline:
            if '//' in blob.name:
                try:
                    BlobManager.move_file_to_trash(blob.name, BlobsContainers.timeline.value)
                    print(blob.name)
                    delete += 1
                except:
                    print('Error sending file to trash')

        if next_marker == '':
            print('Clean')
            break
        
        print("deleted: {} of {}".format(delete, 1000))

        next_marker = timeline.next_marker
