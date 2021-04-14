import requests
#import logging
import json
from tinydb import TinyDB

class Cats():
    def __init__(self):
        self.document = {}
        self.data = requests.get("http://api.thecatapi.com/v1/breeds", verify=False)
        self.db = TinyDB('nosql.db')
        self.protocol = 'http'
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s] %(levelname)s in %(module)s: %(message)s')

    def getCatsInfo(self):
        #logging.info("Coletando informações das raças")
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

    def getCatsImages(self, tipo):

        limiteImagens = 3
        if 'raca' in tipo:
            #logging.info("Coletando imagens das raças")
            for cats in json.loads(self.data.content):
                try:
                    id = cats['id']
                    response = requests.get(f"{self.protocol}://api.thecatapi.com/v1/images/search?breed_id={id}&limit={limiteImagens}")
                    imageUrl = json.loads(response.content)
                    imagens = []
                    for items in range(len(imageUrl)):
                        imagens.append(imageUrl[items]['url'])
                    cat = {
                        'imagesUrl': imagens
                    }
                    if id in self.document:
                        self.document[id][0].update(cat)
                    else:
                        self.document = [cat]

                except Exception as ex:
                    #print(f'{ex}: para a raça: {id}')
                    continue
        elif 'chapeu' in tipo:
            #logging.info("Coletando imagens de gatos de chapéu")
            category_id = '1'
            response = requests.get(f"{self.protocol}://api.thecatapi.com/v1/images/search?category_ids={category_id}&limit={limiteImagens}")
            imageUrl = json.loads(response.content)
            imagensChapeu = []
            for items in range(0, limiteImagens):
                imagensChapeu.append(imageUrl[items]['url'])
            self.document['imagensChapeu'] = imagensChapeu

        elif 'oculos' in tipo:
            #logging.info("Coletando imagens de gatos de oculos")
            category_id = '4'
            response = requests.get(f"{self.protocol}://api.thecatapi.com/v1/images/search?category_ids={category_id}&limit={limiteImagens}")
            imageUrl = json.loads(response.content)
            imagensOculos = []
            for items in range(0, limiteImagens):
                imagensOculos.append(imageUrl[items]['url'])
            self.document['imagensOculos'] = imagensOculos

    def insertToDB(self):

        self.db.insert(self.document)
    def queryDB(self):
        pass

    def main(self):

        self.getCatsInfo()
        self.getCatsImages(tipo='raca')
        self.getCatsImages(tipo='chapeu')
        self.getCatsImages(tipo='oculos')
        #Descomente a linha abaixo para gravar o banco em um arquivo
        self.insertToDB()
        #self.queryDB()

if __name__ == '__main__':
    x = Cats()
    x.main()
    print(x.document)