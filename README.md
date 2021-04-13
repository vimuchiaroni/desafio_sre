# SRE

- App

A aplicação consiste em uma classe CATS que busca dados the cat API(https://thecatapi.com) e insere os dados de interesse em um documento em memória

- API

A api, por sua vez, importa a classe cats e utiliza o documento resultante como um banco de dados em memória.
A documentação da api pode ser encontrada [aqui](https://vimuchiaroni.github.io)

## Rodando localmente

- Opção 1
    
    Utilizando docker, rode o container disponibilizado no DockerHub
    
    ```
    # docker run -p 5000:8000 vimuchiaroni/desafio_sre:latest
    ```

- Opção 2

    1. Clonar o projeto do Github:
        ```
        # git clone https://github.com/vimuchiaroni/desafio_sre
        ```
    2. Fazer o build da imagem localmente utilizando docker:
        ```
        # cd desafio_sre
        # docker build . -t desafio_sre:latest
        ``` 
    3. Rodar o container:
        ```
        # docker run -p 5000:8000 vimuchiaroni/desafio_sre:latest
         ```   