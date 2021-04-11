import app.collect_data as createDB
from flask import Flask
import logging
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


@app.route('/api/temperamento/<tipo_temperamento>')
def temperamento(tipo_temperamento):
    pass

@app.route('/api/version')
def getVersion():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)