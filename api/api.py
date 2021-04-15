import os
import re
from logging.config import dictConfig

#Logging configuration
#logging.basicConfig(level=logging.INFO, format='%(asctime)s] %(levelname)s in %(module)s: %(message)s')
#logger = logging.getLogger(__name__)


#Flask application configuration
dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


from flask import Flask
from app import collect_data as createDB
from flask import jsonify
from flask import Response
from flask import request
from elasticapm.contrib.flask import ElasticAPM

app_name = 'gatos'
app = Flask(__name__)

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
        app.logger.error(f'Não foi possivel conectar-se ao APM server: {apmErr}')

#Runtime create database
try:
    app.logger.info("Inicializando Database...")
    db = createDB.Cats()
    db.main()
    app.logger.info("Api inicializada com sucesso")
except Exception as dbError:
    app.logger.error(f"Failed to create Database: {dbError}")


@app.route("/api")
def index():
    app.logger.error("Acesso ao /api não permitido")
    return Response(
        "Path não permitido",
        status=400,
    )


@app.route('/api/racas', methods=['get'])
def listaRacas():

    filter = request.args.get('raca')
    try:
        if filter:
            if filter in db.dbraca:
                return jsonify(db.dbraca[filter]), 200
            else:
                return jsonify({})
        else:
            return jsonify(db.dbraca), 200
    except Exception as err:
        return jsonify("Não foi possivel carregar as  raças"), 400


@app.route('/api/temperamento', methods=['get'])
def getTemperamento():
    tipo_temperamento = request.args.get('temperamento')
    gatos = {}
    try:
        if tipo_temperamento:
            for gato in db.dbraca:
                if re.search(rf'\b{tipo_temperamento}\b', db.dbraca[gato][0]['temperamento'], flags=re.IGNORECASE):
                    gatos[gato] = db.dbraca[gato]
        else:
            temperamentos = []
            for racas in db.dbraca:
                for temperamento in db.dbraca[racas][0]['temperamento'].split(','):
                    if temperamento.strip().lower() not in temperamentos:
                        temperamentos.append(temperamento.strip().lower())
            return jsonify(f'Temperamentos Disponiveis: {temperamentos}'), 200
    except Exception as err:
        app.logger.error(f'Não foi possivel carregar os temperamentos: {err}')
        return jsonify(f'Não foi possivel carregar os temperamentos: {err}'), 400
    return gatos, 200
@app.route('/api/origem', methods=['get'])
def getOrigem():
    origem = request.args.get('origem')
    gatos = {}
    try:
        if origem:

            for gato in db.dbraca:

                    if re.search(rf'\b{origem}\b', db.dbraca[gato][0]['origem'], flags=re.IGNORECASE):
                        gatos[gato] = db.dbraca[gato]
        else:
            origens = []
            for racas in db.dbraca:
                for paises in db.dbraca[racas][0]['origem'].split(','):
                    if paises.strip().lower() not in origens:
                        origens.append(paises.strip().lower())
            return jsonify(f'Origens Disponiveis: {origens}'), 200
    except Exception as err:
        app.logger.error(f'Não foi possivel carregar as origens: {err}')
        return jsonify(f'Não foi possivel carregar as origens: {err}'), 400


    return gatos, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)