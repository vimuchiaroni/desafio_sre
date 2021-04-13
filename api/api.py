import os
import logging
import re
from flask import Flask
from app import collect_data as createDB
from flask import jsonify
from flask import Response
from flask import request
from elasticapm.contrib.flask import ElasticAPM
from logging.config import dictConfig

#Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s] %(levelname)s in %(module)s: %(message)s')

#Flask application configuration
app_name = 'gatos'
app = Flask(app_name)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
if 'ELASTIC_SERVER' in os.environ:
    if 'ELASTIC_TOKEN' in os.environ:
        apmConfig = {
          'SERVICE_NAME': app_name,
          # Use if APM Server requires a secret token
          'SECRET_TOKEN': os.environ['ELASTIC_TOKEN'],
          # Set the custom APM Server URL (default: http://localhost:8200)
          'SERVER_URL': os.environ['ELASTIC_SERVER'],
          # Set the service environment
          'ENVIRONMENT': 'production',
          'VERIFY_SERVER_CERT': 'False'
        }
    else:
        apmConfig = {
          'SERVICE_NAME': app_name,
          # Set the custom APM Server URL (default: http://localhost:8200)
          'SERVER_URL': os.environ['ELASTIC_SERVER'],
          # Set the service environment
          'ENVIRONMENT': 'production',
          'VERIFY_SERVER_CERT': 'False'
        }
    try:
        app.config['ELASTIC_APM'] = apmConfig
        apm = ElasticAPM(app, logging=True)
    except Exception as apmErr:
        logging.error(f'Não foi possivel conectar-se ao APM server: {apmErr}')

#Runtime create database
try:
    logging.info("Initializing Database...")
    db = createDB.Cats()
    db.main()
    logging.info("Database created successfully")
except Exception as dbError:
    logging.error(f"Failed to create Database: {dbError}")


@app.route("/api")
def index():
    logging.error("Não permitido")
    return Response(
        "Path não permitido",
        status=400,
    )


@app.route('/api/racas', methods=['get'])
def listaRacas():

    filter = request.args.get('raca')
    if filter:
        try:
            return jsonify(db.document[filter]), 200
        except Exception as err:
            return jsonify("Raça não encontrada"), 204
    else:
        return jsonify(db.document), 200


@app.route('/api/temperamento', methods=['get'])
def getTemperamento():
    tipo_temperamento = request.args.get('temperamento')
    gatos = {}
    if tipo_temperamento:

            for gato in db.document:
                try:
                    if re.search(rf'\b{tipo_temperamento}\b', db.document[gato][0]['temperamento'], flags=re.IGNORECASE):
                        gatos[gato] = db.document[gato]
                except Exception as err:
                    continue


    else:
        temperamentos = []
        for racas in db.document:
            try:
                for temperamento in db.document[racas][0]['temperamento'].split(','):
                    if temperamento.strip().lower() not in temperamentos:
                        temperamentos.append(temperamento.strip().lower())
            except Exception as err:
                logging.error(f'Erro ao listar raças: {err} {racas}'), 500
                continue
        return jsonify(f'Temperamentos Disponiveis: {temperamentos}'), 200

    return gatos, 200
@app.route('/api/origem', methods=['get'])
def getOrigem():
    origem = request.args.get('origem')
    gatos = {}
    if origem:

        for gato in db.document:
            try:
                if re.search(rf'\b{origem}\b', db.document[gato][0]['origem'], flags=re.IGNORECASE):
                    gatos[gato] = db.document[gato]
            except Exception as err:
                continue

    else:
        origens = []
        for racas in db.document:
            try:
                for paises in db.document[racas][0]['origem'].split(','):
                    if paises.strip().lower() not in origens:
                        origens.append(paises.strip().lower())
            except Exception as err:
                continue
        return jsonify(f'Origens Disponiveis: {origens}'), 200

    return gatos, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)