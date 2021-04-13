# Github scanner
[![codecov](https://codecov.io/gh/eynan/github-scanner/branch/main/graph/badge.svg?token=SGO58COXY0)](https://codecov.io/gh/eynan/github-scanner)  [![Tests](https://github.com/eynan/github-scanner/actions/workflows/python-app.yml/badge.svg)](https://github.com/eynan/github-scanner/actions/workflows/python-app.yml)

## Install
Using docker and docker composer.\
I used docker engine 20.10 and compose 1.27
```
docker-compose up -d
docker-compose exec backend python manage.py migrate
````
Se preferir instalar localmente utilizado python versão 3.9 e o banco de dados postgreSQL 12
```
pip install -r requirements.txt
python manage.py migrate
```

For run tests
```
 docker-compose exec backend python manage.py test
```

## Tecnical detail

### screper
For run the screper.

```
docker-compose exec backend python githubscanner.py
```
A cada vez que executar esse script ele obtem na api do github 30 usuarios e seus repositorios, nas proximas vezes que executar o script
ele vai continuar a partir do ultimo usuario que ele tiver salvo no banco de dados. Eu limitei em 30 usuarios porque o github limita os requests
sem autorização em 60 requests por hora, mas caso estrapole a quantidade de requests do github o programa está preparado para esperar o tempo
do bloqueio terminar e continuar fazendo as consultas.

### api
Criei dois endpoints GET:
```
http://localhost:8000/users
http://localhost:8000/repositories
```
Ambos endpoints possuem paginação, por padrão limito em 100 registros por pagina mas é possivel passar a paginação por parametros.
ex:
```url
 http://localhost:8000/repositories?per_page=5&page=5
```
