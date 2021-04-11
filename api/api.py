import app.collect_data as createDB
import logging
logging.info("Initializing Database...")
db = createDB.Cats()
db.main()

for item in db.document:
    print(db.document[item][0].nome)
