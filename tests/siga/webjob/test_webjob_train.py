from tests.conn import test_mongodb
from datetime import datetime


def test_should_get_documents_with_interval(test_mongodb):
    docs = [
            {'time': datetime(2018, 8, 20, 2, 12, 34),
             'cnpj': '00000000001',
             'feature': 'Feature_1',
             'product': 'AA',
             'user': 'USER_2',
             'instanceId': 2,
             'machine': 'MACHINE_2',
             'rowType': 'Activate'
             },
            {'time': datetime(2018, 8, 20, 2, 12, 34),
             'cnpj': '00000000001',
             'feature': 'Feature_1',
             'product': 'AA',
             'user': 'USER_3',
             'instanceId': 3,
             'machine': 'MACHINE_3',
             'rowType': 'Activate'
             }
            ]

    start_interval = datetime(2018, 8, 20, 0, 0, 0)
    end_interval = datetime(2018, 8, 21, 0, 0, 0)

    cursor = test_mongodb.TimeLine.find({'rowType': 'Activate', 'time':
        {'$gt': start_interval, '$lt': end_interval}}).batch_size(1000)

    n = cursor.count()
    documents = [cursor.next() for _ in range(n)]

    for doc in documents:
        doc.pop('_id', None)

    assert documents == docs
