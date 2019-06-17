import json
from azure.storage.blob import BlockBlobService
from azure.common import AzureMissingResourceHttpError

from src.utils.log import Log
from enum import Enum
from os import getenv

log = Log()


class BlobsContainers(Enum):
    cycles = 'cycles'
    models = 'models'
    timeline = 'timeline'
    paths = 'paths'


class ModelType(Enum):

    def __str__(self):
        return str(self.value)

    user = 'user'
    product = 'product'
    cnpj = 'cnpj'


class BlobManager:
    account_name = getenv("BLOBS_NAME")
    account_key = getenv("BLOBS_KEY")
    container_name = BlobsContainers.timeline.value
    block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

    @staticmethod
    def save_document_as_blob(document, container=BlobsContainers.models.value):
        """

        :param document:  Nome do documento a ser salvo no Azure Blobs
        :param container:  O nome do container no qual o documento será salvo

        """
        product = document[ModelType.product.value]
        cnpj = document[ModelType.cnpj.value] if ModelType.cnpj.value in document else None
        user = document[ModelType.user.value] if ModelType.user.value in document else None

        if '_id' in document:
            document.pop('_id')

        filepath = BlobManager.file_path(product, cnpj, user)
        BlobManager.create_blob_from_text(filepath, json.dumps(document, ensure_ascii=False), blob_container=container)

    @staticmethod
    def file_path(product=None, cnpj=None, user=None):
        """

        :param product:  Nome do produto
        :param cnpj:  Número do CNPJ da empresa requisitante. Este atributo é opcional
        :param user:  Nome do Usuário requisitante. Este atribuito é opcional
        :return É retornado o caminho do arquivo onde se encontra o modelo referente aos dados passados por parâmetro.

        """
        document_path = ""

        custom_model_name = product
        custom_model_name += cnpj if cnpj is not None else ""
        custom_model_name += user if user is not None else ""

        if product is not None:
            document_path += product
            if cnpj is not None:
                document_path += '/' + cnpj
                if user is not None:
                    document_path += '/' + user
                else:
                    document_path += '/' + cnpj
            else:
                document_path += '/' + product

        return document_path + '.json'

    @staticmethod
    def retrieve_blob_with_document_name(document_name, container=BlobsContainers.models.value):
        """

        :param document_name: caminho do arquivo a ser requisitado
        :param container:  O nome do container no qual o documento está salvo
        :return É retornado blob no formato JSON com o modelo

        """
        try:
            blob = BlobManager.find_blob(document_name, container=container)
        except Exception as e:
            log.error(e)
            raise e

        if blob is None:
            return blob
        else:
            try:
                blob_decoded = json.loads(blob.content.decode('utf-8'))
                return blob_decoded, blob
            except Exception as e:
                log.error(e)
                return None, blob

    @staticmethod
    def retrieve_zip_blob_with_document_name(document_name):

        """
        Esta função sempre busca arquivos zip no container Timeline
        :param document_name: caminho do arquivo a ser requisitado
        :return É retornado blob no formato JSON com dados de sequencias descompactados

        """

        try:
            blob = BlobManager.find_blob(document_name)
        except Exception as e:
            log.error(e)
            raise e

        if blob is None:
            return None
        return blob.content

    @staticmethod
    def retrieve_blob_with_document_data(product=None, cnpj=None, user=None,
                                         container=BlobsContainers.models.value):

        """
        :param product:  Nome do produto
        :param cnpj:  Número do CNPJ da empresa requisitante. Este atributo é opcional
        :param user:  Nome do Usuário requisitante. Este atribuito é opcional
        :param container:  O nome do container no qual o documento está salvo

        :return É retornado blob no formato JSON com o modelo de transições

        """

        blobname = BlobManager.file_path(product=product, cnpj=cnpj, user=user)
        try:
            blob = BlobManager.find_blob(blobname, container=container)
        except Exception as e:
            log.error(e)
            raise e

        if blob is None:
            return None
        else:
            try:
                blob = json.loads(blob.content.decode('utf-8'))
                return blob
            except Exception as e:
                log.error(e)
                return None

    @staticmethod
    def create_blob_from_text(blob_name, blob_string, blob_container=BlobsContainers.models.value):

        """
        :param blob_name:  Nome do arquivo blob
        :param blob_string:  Dados a serem escritos no blob
        :param blob_container:  O nome do container no qual o documento está salvo

        """

        BlobManager.block_blob_service.create_blob_from_text(blob_container, blob_name, blob_string)

    @staticmethod
    def create_blob_with_path(blob_path, blob_name=None):

        blob_name = blob_name if blob_name is not None else blob_path
        BlobManager.block_blob_service.create_blob_from_path(BlobManager.container_name, blob_name, blob_path)

    @staticmethod
    def list_all_blobs(container_name=container_name, prefix=None, marker=None, num_results=50):

        """
        :param marker:  Utilizado para a paginação dos dados
        :param prefix:  Seleciona apenas os resultados que começam com o valor informado
        :param container_name:  Nome do container onde pesquisar
        :param num_results: Número máximo de resultados a serem requisitados

        """

        generator = BlobManager.block_blob_service.list_blobs(container_name=container_name, prefix=prefix,
                                                              marker=marker, num_results=num_results)

        names = []

        for blob in generator:
            if '//' not in blob.name:
                names.append(blob.name)

        return names, generator.next_marker

    @staticmethod
    def blob_exists(filename, container_name=container_name):

        """
        :param filename:  Nome do blob a ser pesquisado
        :param container_name:  Nome do container onde pesquisar
        :return retorna positivo caso exista ou falso caso não exista
        """

        try:
            BlobManager.block_blob_service.get_blob_to_bytes(container_name, filename)
            return True
        except AzureMissingResourceHttpError:
            return False
        except Exception as e:
            log.error("Unknown error in blob_exists: {}".format(e))
            raise e

    @staticmethod
    def move_file_to_trash(blob_name, container):

        """
            :param blob_name:  Nome do arquivo a ser apagado
            :param container: Nome do container onde o arquivo deve ser encontrado
        """
        try:
            BlobManager.block_blob_service.delete_blob(container, blob_name)
        except Exception as e:
            raise e

    @staticmethod
    def find_blob(blob_name, container=container_name):

        """
        :param blob_name:  Nome do blob a ser encontrado
        :param container:  Nome do container onde pesquisar
        :return retorna o arquivo do blob no formato de bytes
        """

        try:
            if BlobManager.blob_exists(blob_name, container):
                return BlobManager.block_blob_service.get_blob_to_bytes(container, blob_name)
            else:
                return None
        except Exception as e:
            log.error(e)
            raise e


    @staticmethod
    def get_container_size(container_name):

        """
            :param container_name:  Nome do container cujo tamanho será retornado
            :return retorna o tamanho do container e o número de arquivos contidos nele
        """
        marker = None
        cont_size = 0
        cont_num = 0
        while marker != "":
            generator = BlobManager.block_blob_service.list_blobs(container_name, marker=marker)
            marker = generator.next_marker
            for blob in generator:
                cont_size += blob.properties.content_length
                cont_num += 1

        print(container_name + " : " + str(cont_size / 1000000) + " MB" + " in " + str(cont_num) + " blobs")

        return cont_size, cont_num
