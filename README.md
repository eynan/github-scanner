# Github scanner
[![codecov](https://codecov.io/gh/eynan/github-scanner/branch/main/graph/badge.svg?token=SGO58COXY0)](https://codecov.io/gh/eynan/github-scanner)  [![Tests](https://github.com/eynan/github-scanner/actions/workflows/python-app.yml/badge.svg)](https://github.com/eynan/github-scanner/actions/workflows/python-app.yml)

## Install
Using docker and docker composer.\
I used docker engine 20.10 and compose 1.27
```
docker-compose up -d
docker-compose exec backend python manage.py migrate
````
If you prefer you can install locally used python version 3.9 and the postgreSQL 12 database.
```
pip install -r requirements.txt
python manage.py migrate
```

For run tests:
```
 docker-compose exec backend python manage.py test
```

## Technical details

### screper
For run the screper:
```
docker-compose exec backend python githubscanner.py
```
Each time you run this script it gets 30 users and their repositories from the Github api, the next time you run the script it will continue from the last user it has saved to the database. I limited it to 30 users because Github limits the number of requests without authorization to 60 requests per hour, but if it exceeds the number of requests from Github, the program is prepared to wait for the blocking time to end and continue making queries.

### api
I created two endpoints GET:
```
http://localhost:8000/users
http://localhost:8000/repositories
```
 **Pagination**\
 Both endpoints have pagination, by default limited to 100 records maximum per page but it is possible to pass the number of records by parameters.
`per_page` and `page`
```url
 http://localhost:8000/repositories?per_page=5&page=5
```
**Ordering**\
Sorting it is possible to sort by any returned record using the parameter `order_by = {field}` and for descending ordering `order_by = - {field}`
ex:
```url
 http://localhost:8000/repositories?per_page=5&page=5
```
**filtros**\
All **integer** and **datetime** fields in addition to the equality filter also implement other operations such as [`__gt`,`__gte`, `__lt`,`__lte`,].
ex:
```
http://localhost:8000/repositories?user__gte=6&watchers_count__gt=5
http://localhost:8000/users?login=mojombo   
```
Users

| Field    |    type    |
|----------|:-------------:|
| id |  integer |
| user |    String   |
Repositories

| Field    |    type    |
|----------|:-------------:|
| id |  integer |
| user|    integer   |
| name|    String   |
| language|    String   |
| forks_count|    Integer   |
| stargazers_count|    Integer   |
| watchers_count|    Integer   |
| created_at|    DateTime  |
| updated_at|    DateTime   |
| pushed_at|    DateTime   |
