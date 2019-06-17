from src.utils.log import Log
from src.utils.storage.blobs import BlobManager
from azure.common import AzureMissingResourceHttpError

blob_manager = BlobManager()
log = Log()


def create_entity(model, container):
    blob_manager.save_document_as_blob(model, container=container)


def delete_entity(entity, container):
    try:
        BlobManager.move_file_to_trash(entity, container)
    except AzureMissingResourceHttpError as nf:
        log.error('Falha ao deletar blob: {}'.format(nf))
    except Exception as e:
        log.error("Erro desconhecido ao deletar blob: {}".format(e))


def update(model, container):
    blob_manager.save_document_as_blob(model, container=container)


def find_one(product, cnpj=None, user=None):
    return blob_manager.retrieve_blob_with_document_data(product, cnpj, user)
