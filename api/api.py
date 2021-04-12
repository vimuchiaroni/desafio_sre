import app.collect_data as createDB
from flask import Flask
import logging
import re
from flask import jsonify
from flask import request

#Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

#Flask application configuration
app_name = 'gatos'
app = Flask(app_name)
app.debug = True

#Runtime create database
try:
    logging.info("Initializing Database...")
    db = createDB.Cats()
    db.main()
    logging.info("Database created successfully")
except Exception as dbError:
    logging.error(f"Failed to create Database: {dbError}")


@app.route('/api/racas', methods=['get'])
def listaRacas():

    filter = request.args.get('raca')
    if filter:
        try:
            return jsonify(db.document[filter])
        except Exception as err:
            return jsonify("Raça não encontrada")
    else:
        return jsonify(db.document)


@app.route('/api/temperamento', methods=['get'])
def getTemperamento():
    tipo_temperamento = request.args.get('temperamento')
    gatos = {}
    if tipo_temperamento:
        try:
            for gato in db.document:
                if re.search(rf'\b{tipo_temperamento}\b', db.document[gato][0]['temperamento'], flags=re.IGNORECASE):
                    gatos[gato] = db.document[gato]
        except Exception as err:
            return jsonify("Nenhum gato encontrado com o temperamento informado")

    else:
        temperamentos = []
        for racas in db.document:
            for temperamento in db.document[racas][0]['temperamento'].split(','):
                if temperamento.strip() not in temperamentos:
                    temperamentos.append(temperamento.strip())
        return jsonify(f'Temperamentos Disponiveis: {temperamentos}')





    return gatos
@app.route('/api/origem', methods=['get'])
def getOrigem():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)