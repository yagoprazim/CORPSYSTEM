# 🚀 CORPSYSTEM (Teste técnico)

Trata-se de um projeto fullstack com o uso de Django Rest Framework, Vue.js, MySql, Docker.

## Requerimentos
- Python 3+
- NodeJS
- Docker

## Tutorial
``` bash
git clone https://github.com/yagoprazim/CORPSYSTEM.git #Clone o repositório.
cd .\CORPSYSTEM\ #Acesse a pasta raiz do projeto;
docker-compose up --build #Comando para rodar o docker

#Para ter acesso à área admin e aos endpoints, você precisa estar autenticado, portanto, crie um superuser:
docker exec -it django-backend /bin/bash
python manage.py createsuperuser
```
Obs.: Resolvi deixar os arquivos de configuração no repositório para facilitar... (settings.json: para o back-end, .env: para o front-end)
## Endpoints Gerais:
- Através do endpoint de login: http://localhost:8000/api/login/ - você fornecerá o user registrado na área admin, para ter acesso aos endpoints principais da API, os quais você consegue ver a partir de: http://localhost:8000/api/ - O interessante do uso do Django Rest Framework + Viewsets, é que o próprio django fornecesse um template intuitivo para gerenciar e testar os endpoints da API, permitindo realização de CRUD's completos dos endpoints.

- Obs.: Recomenda-se antes de utilizar os endpoints da API, vincular o usuário logado a um vendedor, para que ele possa acessar livremente os endpoints relativos às vendas (trata-se de uma permission que fiz). Para isso, basta acessar:
http://localhost:8000/admin/    --> Aqui, você pode criar novos vendedores/users, como também, users que não são vendedores. Inclusive, através da área admin, pode-se realizar a maioria dos cruds da api, sendo uma forma rápida e fácil de lidar com a criação dos dados, com uma interface customizada através do jazzmin.

- O endpoint principal do front-end é o: http://localhost:3000/ - a partir dele, você realiza login com o user que foi cadastrado na área admin da API. Com o login feito, a interface se torna mais intuitiva através dos menus do header.

## Vídeo com explicações mais detalhadas sobre os endpoints, tela de admin e front-end:
Google Drive: https://drive.google.com/file/d/1yRAH_xQ6sGUx7FE3Ko1DtD4TR4ERqxGV/view?usp=sharing

## Tests:
Os testes do back-end encontram-se no arquivo tests.py.
Para rodá-los, basta:
``` bash
py manage.py test
```
