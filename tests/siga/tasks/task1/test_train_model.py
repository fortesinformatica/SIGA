from src.tasks.task1.train_model import *
from tests.conn import test_mongodb
from datetime import datetime
from src.utils.conn import get_model
from src.utils import blobs_service as service

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


def _Ignore_test_should_get_user():
    docs = [
            {'cnpj': '00000000001',
             'product': 'AA',
             'user': 'USER_1',
             'model': {
                'frame1': {
                    'frame11': 37,
                    'frame1': 5,
                    'frame13': 28,
                    'frame12': 4
                },
                'frame11': {
                    'frame1': 28,
                    'frame2': 4
                },
                'frame13': {
                    'frame1': 5,
                    'frame3': 11,
                    'frame2': 4
                },
                'frame121': {
                    'frame221': 6
                },
                'frame221': {
                    'frame121': 1
                },
                'frame2': {
                    'frame21': 8
                },
                'frame3': {
                    'frame31': 15
                },
                'frame12': {
                    'frame1': 4
                },
                'frame21': {
                    'frame3': 4
                }
             },
             'accuracy': {
                 'day': 20,
                 'total': 36,
                 'historic':[
                     [0.0, 0.0, 0.0, 0.0, 0.0], 
                     [0.18, 0.18, 0.37, 0.37, 0.37], 
                     [0.37, 0.49, 0.5, 0.52, 0.52], 
                     [0.43, 0.55, 0.58, 0.62, 0.62], 
                     [0.22, 0.63, 0.63, 0.63, 0.63]
                 ], 
                 'hits': [0.43, 0.55, 0.58, 0.62, 0.62], 
             },
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

    user = 'USER_1'
    cnpj = '00000000001'
    product = 'AA'

    user_model = service.find_one(product=product, cnpj=cnpj, user=user)
    assert docs[0] == user_model

    # user = get_model(user_id='USER_1', cnpj_id='00000000001', prod_id='AA')
    # assert user['cnpj'] == docs[0]['cnpj'] and user['product'] == docs[0]['product'] and user['user'] == docs[0]['user']


def _Ignore_test_should_get_user_in_cnpj():
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


def _Ignore_test_should_get_user_in_product():
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

    user_teste_collection=test_mongodb.Models
    print(user_teste_collection)
    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_user(user_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'product': product})

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
    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_user(user_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_user(user_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'product': product})

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

    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_user(user_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj + user, 'product': product})

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

    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_cnpj(cnpj_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'product': product})

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

    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_cnpj(cnpj_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'product': product})

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

    #Converter a propriedade time para string, porque a procedure train_user espera ela como string
    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_cnpj(cnpj_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_cnpj(cnpj_data = docs)
    
    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_cnpj(cnpj_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product + cnpj, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_product(product_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_product(product_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_product(product_data = docs)

    model = test_mongodb.Models.find_one({'model_id': product, 'product': product})

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

    docs[0]['time'] = docs[0]['time'].strftime('%Y-%m-%dT%H:%M:%S')
    train_product(product_data = docs)

    # train_product(product='AA', documents=docs, last_sessions_product={}, product_collection=test_mongodb.Models)

    model = test_mongodb.Models.find_one({'model_id': product, 'product': product})

    assert model['model'] == expected_model

