from src import app
from enum import Enum
from werkzeug.exceptions import (
    HTTPException,
    NotFound,
    Forbidden,
    InternalServerError,
    BadRequest,
    MethodNotAllowed
)
from werkzeug.wrappers import Response

import json


@app.errorhandler(HTTPException)
def http_exception(error):
    return Response(
        json.dumps(ensure_ascii=False, obj={
            'error': error.code,
            'details': error.description,
            'message': 'Erro ao processar a requisição. {}'.format(APIException.get_details(error))
        }),
        mimetype='application/json',
        status=error.code
    )


class APIException(Enum):

    BAD_REQUEST = (BadRequest.__name__, 'O pedido não pôde ser entregue devido à sintaxe incorreta.')
    FORBIDDEN = (Forbidden.__name__, 'Você não está autorizado a acessar esta página.')
    INTERNAL_SERVER_ERROR = (InternalServerError.__name__, 'Erro interno no servidor ao processar a solicitação.')
    METHOD_NOT_ALLOWED = (MethodNotAllowed.__name__, 'Foi feita uma solicitação de um recurso usando um método de '
                                                     'pedido que não é compatível com esse recurso, por exemplo,'
                                                     'usando GET em um formulário, que exige que os dados a serem '
                                                     'apresentados via POST, PUT ou usar em um recurso somente de '
                                                     'leitura.')
    NOT_FOUND = (NotFound.__name__, 'O recurso requisitado não foi encontrado.')

    def __init__(self, error_name, message):
        self.error_name = error_name
        self.message = message

    @property
    def get_error_name(self):
        return self.error_name

    @property
    def get_message(self):
        return self.message

    @classmethod
    def get_items(cls):
        return list(cls.__members__.items())

    @classmethod
    def get_details(cls, error=NotFound):
        tmp = list(map(lambda x: x[1], APIException.get_items()))
        exceptions = [error.get_error_name for error in tmp]
        descriptions = [error.get_message for error in tmp]

        if error.__class__.__name__ in exceptions:
            idx = exceptions.index(error.__class__.__name__)
            return descriptions[idx]
        else:
            return 'Erro na requisição.'
