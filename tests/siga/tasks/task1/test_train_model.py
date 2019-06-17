from src.tasks.task1.train_model import *
from tests.conn import test_mongodb
from datetime import datetime


def test_should_sum_empty_models():

    update_model = {}
    actual_model = {}

    new_model = sum_models(update_model, actual_model)

    assert new_model == {}


def test_should_sum_empty_model_with_non_empty_model():
    update_model = {'feature_1': {'feature_11': 1,
                                  'feature_12': 1
                                  },
                    'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  }
                    }

    actual_model = {}

    new_model = sum_models(update_model, actual_model)

    assert new_model == update_model


def test_should_sum_two_equal_models():
    update_model = {'feature_1': {'feature_11': 1,
                                  'feature_12': 1
                                  },
                    'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  }
                    }

    actual_model = {'feature_1': {'feature_11': 1,
                                  'feature_12': 1
                                  },
                    'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  }
                    }

    new_model = sum_models(update_model, actual_model)

    assert new_model == {'feature_1': {'feature_11': 2,
                                       'feature_12': 2
                                       },
                         'feature_2': {'feature_21': 2,
                                       'feature_22': 2
                                       }
                         }


def test_should_sum_two_different_models():
    update_model = {'feature_1': {'feature_11': 1,
                                  'feature_12': 1
                                  },
                    'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  }
                    }

    actual_model = {'feature_3': {'feature_31': 1,
                                  'feature_32': 1
                                  },
                    'feature_4': {'feature_41': 1,
                                  'feature_42': 1
                                  }
                    }

    new_model = sum_models(update_model, actual_model)

    assert new_model == {'feature_1': {'feature_11': 1,
                                       'feature_12': 1
                                       },
                         'feature_2': {'feature_21': 1,
                                       'feature_22': 1
                                       },
                         'feature_3': {'feature_31': 1,
                                       'feature_32': 1
                                       },
                         'feature_4': {'feature_41': 1,
                                       'feature_42': 1
                                       }
                         }


def test_should_sum_two_almost_different_models():
    update_model = {'feature_1': {'feature_11': 1,
                                  'feature_12': 1
                                  },
                    'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  }
                    }

    actual_model = {'feature_2': {'feature_21': 1,
                                  'feature_22': 1
                                  },
                    'feature_3': {'feature_31': 1,
                                  'feature_32': 1
                                  }
                    }

    new_model = sum_models(update_model, actual_model)

    assert new_model == {'feature_1': {'feature_11': 1,
                                       'feature_12': 1
                                       },
                         'feature_2': {'feature_21': 2,
                                       'feature_22': 2
                                       },
                         'feature_3': {'feature_31': 1,
                                       'feature_32': 1
                                       }
                         }


def test_should_get_user():
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

    user = get_user(user='USER_2', product='AA', cnpj='00000000001', data=docs)

    assert user == [docs[0]]


def test_should_get_user_in_cnpj():
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
             },
            {'time': datetime(2018, 8, 20, 2, 12, 34),
             'cnpj': '00000000002',
             'feature': 'Feature_1',
             'product': 'AA',
             'user': 'USER_4',
             'instanceId': 3,
             'machine': 'MACHINE_4',
             'rowType': 'Activate'
             }
            ]

    users = get_cnpj(product='AA', cnpj='00000000001', data=docs)

    assert users == docs[0:2]


def test_should_get_user_in_product():
    docs = [
            {'time': datetime(2018, 8, 20, 2, 12, 34),
             'cnpj': '00000000001',
             'feature': 'Feature_1',
             'product': 'AB',
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
             },
            {'time': datetime(2018, 8, 20, 2, 12, 34),
             'cnpj': '00000000002',
             'feature': 'Feature_1',
             'product': 'AA',
             'user': 'USER_4',
             'instanceId': 3,
             'machine': 'MACHINE_4',
             'rowType': 'Activate'
             }
            ]

    users = get_product(product='AA', data=docs)

    assert users == docs[1:3]


def test_should_train_user_updating_transition(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    user = 'USER_1'
    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 2,
                           'frame12': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2}
                      }

    train_user(user='USER_1', cnpj='00000000001', product='AA', documents=docs,
               last_sessions_user={}, user_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'partitionKey': product})

    assert expected_model == model['model']


def test_should_train_user_adding_new_transition(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    user = 'USER_1'
    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2}
                      }

    train_user(user='USER_1', cnpj='00000000001', product='AA', documents=docs,
               last_sessions_user={}, user_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_user_with_different_instanceid(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    user = 'USER_1'
    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 2},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2}
                      }

    train_user(user='USER_1', cnpj='00000000001', product='AA', documents=docs,
               last_sessions_user={}, user_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_user_with_last_session(test_mongodb):

    last_session = {
        1: {'time': datetime(2018, 8, 20, 1, 10, 34),
            'cnpj': '00000000001',
            'feature': 'frame12',
            'product': 'AA',
            'user': 'USER_1',
            'instanceId': 1,
            'machine': 'MACHINE_1',
            'rowType': 'Activate'
        },
        2: {'time': datetime(2018, 8, 20, 1, 20, 34),
            'cnpj': '00000000001',
            'feature': 'frame22',
            'product': 'AA',
            'user': 'USER_1',
            'instanceId': 2,
            'machine': 'MACHINE_1',
            'rowType': 'Activate'
        }
    }

    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    user = 'USER_1'
    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1},
                      'frame12':
                          {'frame121': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2},
                      'frame22':
                          {'frame221': 1},
    }

    train_user(user='USER_1', cnpj='00000000001', product='AA', documents=docs,
               last_sessions_user=last_session, user_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_cnpj_updating_transition(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 3,
                           'frame12': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2}
                      }

    train_cnpj(cnpj='00000000001', product='AA', documents=docs,
               last_sessions_cnpj={}, cnpj_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_cnpj_different_users_with_equal_session(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 2,
                           'frame12': 1},
                      'frame2':
                          {'frame21': 3,
                           'frame22': 2}
                      }

    train_cnpj(cnpj='00000000001', product='AA', documents=docs,
               last_sessions_cnpj={}, cnpj_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_cnpj_adding_new_transition(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2},
                      'frame3':
                          {'frame31': 1}
                      }

    train_cnpj(cnpj='00000000001', product='AA', documents=docs,
               last_sessions_cnpj={}, cnpj_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_cnpj_shuffled_users(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 1},
                      'frame2':
                          {'frame21': 3,
                           'frame22': 2}
                      }

    train_cnpj(cnpj='00000000001', product='AA', documents=docs,
               last_sessions_cnpj={}, cnpj_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_cnpj_with_last_session(test_mongodb):

    last_session = {
        'USER_1': {
            1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                'cnpj': '00000000001',
                'feature': 'frame12',
                'product': 'AA',
                'user': 'USER_1',
                'instanceId': 1,
                'machine': 'MACHINE_1',
                'rowType': 'Activate'
            },
            2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                'cnpj': '00000000001',
                'feature': 'frame22',
                'product': 'AA',
                'user': 'USER_1',
                'instanceId': 2,
                'machine': 'MACHINE_1',
                'rowType': 'Activate'
            }
        },
        'USER_2': {
            1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                'cnpj': '00000000001',
                'feature': 'frame12',
                'product': 'AA',
                'user': 'USER_2',
                'instanceId': 1,
                'machine': 'MACHINE_1',
                'rowType': 'Activate'
                },
            2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                'cnpj': '00000000001',
                'feature': 'frame22',
                'product': 'AA',
                'user': 'USER_2',
                'instanceId': 2,
                'machine': 'MACHINE_1',
                'rowType': 'Activate'
                }
        }
    }

    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    cnpj = '00000000001'
    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 1},
                      'frame12':
                          {'frame1': 1,
                           'frame2': 1},
                      'frame22':
                          {'frame1': 1,
                           'frame2': 1},
                      'frame2':
                          {'frame21': 3,
                           'frame22': 2}
    }

    train_cnpj(cnpj='00000000001', product='AA', documents=docs,
               last_sessions_cnpj=last_session, cnpj_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_product_updating_transitions(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 2,
                           'frame12': 1,
                           'frame13': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2},
                      'frame3':
                          {'frame31': 1}
                      }

    train_product(product='AA', documents=docs,
                  last_sessions_product={}, product_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_not_train_product_without_transitions(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1},
                      'frame2':
                          {'frame21': 2,
                           'frame22': 2}
                      }

    train_product(product='AA', documents=docs,
                  last_sessions_product={}, product_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_product_with_last_session(test_mongodb):

    last_session = {
        '00000000001': {
            'USER_1': {
                1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                    'cnpj': '00000000001',
                    'feature': 'frame12',
                    'product': 'AA',
                    'user': 'USER_1',
                    'instanceId': 1,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                },
                2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                    'cnpj': '00000000001',
                    'feature': 'frame22',
                    'product': 'AA',
                    'user': 'USER_1',
                    'instanceId': 2,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                }
            },
            'USER_2': {
                1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                    'cnpj': '00000000001',
                    'feature': 'frame12',
                    'product': 'AA',
                    'user': 'USER_2',
                    'instanceId': 1,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    },
                2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                    'cnpj': '00000000001',
                    'feature': 'frame22',
                    'product': 'AA',
                    'user': 'USER_2',
                    'instanceId': 2,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    }
            }
        },
        '00000000002': {
            'USER_1': {
                1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                    'cnpj': '00000000002',
                    'feature': 'frame12',
                    'product': 'AA',
                    'user': 'USER_1',
                    'instanceId': 1,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    },
                2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                    'cnpj': '00000000002',
                    'feature': 'frame22',
                    'product': 'AA',
                    'user': 'USER_1',
                    'instanceId': 2,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    }
            },
            'USER_2': {
                1: {'time': datetime(2018, 8, 20, 1, 10, 34),
                    'cnpj': '00000000002',
                    'feature': 'frame12',
                    'product': 'AA',
                    'user': 'USER_2',
                    'instanceId': 1,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    },
                2: {'time': datetime(2018, 8, 20, 1, 20, 34),
                    'cnpj': '00000000002',
                    'feature': 'frame22',
                    'product': 'AA',
                    'user': 'USER_2',
                    'instanceId': 2,
                    'machine': 'MACHINE_1',
                    'rowType': 'Activate'
                    }
            }
        }
    }

    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 1,
                           'frame12': 1,
                           'frame13': 2},
                      'frame12':
                          {'frame1': 2,
                           'frame2': 2},
                      'frame22':
                          {'frame1': 2,
                           'frame2': 2},
                      'frame2':
                          {'frame21': 4,
                           'frame22': 2}
    }

    train_product(product='AA', documents=docs,
                  last_sessions_product=last_session, product_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product, 'partitionKey': product})

    assert model['model'] == expected_model


def test_should_train_product_with_all_models(test_mongodb):
    cursor = test_mongodb.TimeLine.find({})
    docs = [docs for docs in cursor]

    product = 'AA'

    expected_model = {'frame1':
                          {'frame11': 4,
                           'frame12': 4,
                           'frame13': 1},
                      'frame2':
                          {'frame21': 4,
                           'frame22': 3},
                      'frame3':
                          {'frame31': 1}
                      }

    train_product(product='AA', documents=docs, last_sessions_product={}, product_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product, 'partitionKey': product})

    assert model['model'] == expected_model

