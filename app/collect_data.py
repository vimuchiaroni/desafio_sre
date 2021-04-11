import requests
import json
#from tinydb import TinyDB

class Cats():
    def __init__(self):
        self.document={}
        self.data = requests.get("https://api.thecatapi.com/v1/breeds")
        #self.db = TinyDB('nosql.db')

    def getCatsInfo(self):

        try:

            for breed in json.loads(self.data.content):
                id = breed['id']
                cat = {
                    "nome": breed['name'],
                    "origem": breed['origin'],
                    "temperamento": breed['temperament'],
                    "descricao": breed['description']
                }
                if id in self.document:
                    self.document[id][0].append(cat)
                else:
                    self.document[id] = [cat]

        except Exception as ex:
            print(ex)

    def getCatsImages(self):

        try:
            for cats in json.loads(self.data.content):
                id = cats['id']
                response = requests.get(f"https://api.thecatapi.com/v1/images/search?breed_id={id}")
                imageUrl = json.loads(response.content)
                cat = {
                    "urlImage": imageUrl[0]['url']
                }

                if id in self.document:
                    self.document[id][0].update(cat)
                else:
                    self.document = [cat]

        except Exception as ex:
            print(ex)

    def insertToDB(self):


        self.db.insert(self.document)
    def queryDB(self):
        pass

    def main(self):

        self.getCatsInfo()
        self.getCatsImages()
        #self.insertToDB()
        #self.queryDB()

if __name__ == '__main__':
    x = Cats()
    x.main()