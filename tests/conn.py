from pymongo import MongoClient
import pytest
import yaml
import os

client = MongoClient()
database = client.test
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def disconnect():
    client.close()


def get_collection(coll_name):
    return database[coll_name]


@pytest.fixture()
def test_mongodb(request):
    path_dataset = request.node.nodeid
    path_dataset = path_dataset.replace("siga", "")
    path_dataset = path_dataset.replace(".py::", "/")
    resources = ROOT_DIR + '/resources'

    test_yml = resources + path_dataset + '.yml'

    stream = open(test_yml, 'r')

    yaml_data = yaml.load(stream)

    for key in yaml_data.keys():
        coll = get_collection(key)
        coll.insert_many(yaml_data[key])

    yield database

    for key in yaml_data.keys():
        coll = get_collection(key)
        coll.drop()

    disconnect()

