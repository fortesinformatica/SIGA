from os import getenv
import sys

from src import app
from src.utils.conn import *
from src.utils import conn
from bson.json_util import dumps
from flask import request


@app.route('/')
def home():
    conn.authenticate_request(request.authorization)
    return 'Welcome to the SIGA project!'


@app.route('/api/product/<prod>')
def get_prod_recommendations(prod):
    conn.authenticate_request(request.authorization)
    models = get_model(prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/cnpj/<cnpj>/product/<prod>')
def get_cnpj_recommendations(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_model(cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/user/<user>/cnpj/<cnpj>/product/<prod>')
def get_user_recommendations(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_model(user_id=user, cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/product/<prod>/cycles')
def get_prod_cycles(prod):
    conn.authenticate_request(request.authorization)
    models = get_cycles_model(prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/cnpj/<cnpj>/product/<prod>/cycles')
def get_cnpj_cycles(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_cycles_model(cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/user/<user>/cnpj/<cnpj>/product/<prod>/cycles')
def get_user_cycles(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_cycles_model(user_id=user, cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)

@app.route('/api/product/<prod>/paths')
def get_prod_path(prod):
    conn.authenticate_request(request.authorization)
    models = get_path_model(prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/cnpj/<cnpj>/product/<prod>/paths')
def get_cnpj_path(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_path_model(cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/api/user/<user>/cnpj/<cnpj>/product/<prod>/paths')
def get_user_path(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_path_model(user_id=user, cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)

@app.route('/storage/api/product/<prod>')
def get_prod_recommendations_storage(prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(prod_id=prod)
    return dumps(models, indent=4)


@app.route('/storage/api/cnpj/<cnpj>/product/<prod>')
def get_cnpj_recommendations_storage(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/storage/api/user/<user>/cnpj/<cnpj>/product/<prod>')
def get_user_recommendations_storage(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(user_id=user, cnpj_id=cnpj, prod_id=prod)
    return dumps(models, indent=4)


@app.route('/storage/api/product/<prod>/cycles')
def get_prod_cycles_storage(prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(prod_id=prod, container=BlobsContainers.cycles)
    return dumps(models, indent=4)


@app.route('/storage/api/cnpj/<cnpj>/product/<prod>/cycles')
def get_cnpj_cycles_storage(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(cnpj_id=cnpj, prod_id=prod, container=BlobsContainers.cycles)
    return dumps(models, indent=4)


@app.route('/storage/api/user/<user>/cnpj/<cnpj>/product/<prod>/cycles')
def get_user_cycles_storage(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(user_id=user, cnpj_id=cnpj, prod_id=prod, container=BlobsContainers.cycles)
    return dumps(models, indent=4)

@app.route('/storage/api/product/<prod>/paths')
def get_prod_path_storage(prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(prod_id=prod, container=BlobsContainers.paths)
    return dumps(models, indent=4)


@app.route('/storage/api/cnpj/<cnpj>/product/<prod>/paths')
def get_cnpj_path_storage(cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(cnpj_id=cnpj, prod_id=prod, container=BlobsContainers.paths)
    return dumps(models, indent=4)


@app.route('/storage/api/user/<user>/cnpj/<cnpj>/product/<prod>/paths')
def get_user_path_storage(user, cnpj, prod):
    conn.authenticate_request(request.authorization)
    models = get_storage_model(user_id=user, cnpj_id=cnpj, prod_id=prod, container=BlobsContainers.paths)
    return dumps(models, indent=4)