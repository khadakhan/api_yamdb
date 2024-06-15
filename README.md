# Rest API DRF
Python API на Django Rest Framework.

Проект позволяет разработчикам интегрировать API 
**социальной сети формата IMDb** через стандартные HTTP-запросы в свои приложения, веб-сайты или другие сервисы.


> [!NOTE]
> С помощью API можно делать аутентификацию, создавать, обновлять, удалять пользователей, произведения, категории, жанры произведений, отзывы на произведения, а также комментарии к отзывам.
## Документация:
> [!TIP] 
> Для чтения документации проекта перейдите по ссылкам Redoc или Swagger после активации сервера
- [Swagger](http://localhost:8000/swagger/) - Доступ к подробной документации по API через Swagger.
- [Redoc](http://localhost:8000/redoc/) - Доступ к подробной документации по API через Redoc.

Также статическую спецификацию можно найти в папке *api_yamdb/static/redoc.yaml*

## Раздел с технологиями

Технологии, используемые в проекте, включают:

- [PYTHON](https://docs.python.org/) - язык программирования.
- [DJANGO](https://www.djangoproject.com/) - веб-фреймворк для разработки веб-приложений на Python.
- [DJANGO REST FRAMEWORK](https://www.django-rest-framework.org/) - библиотека для создания RESTful API на базе Django.
- [SQLITE](https://www.sqlite.org/) (или другая СУБД) - база данных для хранения данных проекта.
- [GIT](https://git-scm.com/) - система контроля версий для управления исходным кодом проекта.
- [SWAGGER](https://swagger.io/) и [REDOC](https://redocly.com/) - инструменты для создания интерактивной документации к API.

## Установка
> [!IMPORTANT]
> Как развернуть проект на локальной машине для разработки и тестирования.

1. Клонировать репозиторий (после fork)
```
git clone git@github.com:<ваше_имя_на_GitHub>/api_yamdb.git
```
2. Создать виртуальное окружение
```
python -m venv venv
```
3. Установить зависимости
```
pip install -r requirements.txt
```
4. Применить миграции
```
python manage.py migrate
```
5. Запустить сервер
```
python manage.py runserver
```
6. Перейти по адресу в своём браузере
```
http://localhost:8000/
```
## Как наполнить БД данными:

```
python manage.py load_from_csv (-f|--files) <Путь до файл(а|лов) .csv> (-m|--model) <Модель в которую нужно загружать содержимое файл(а|ов)>
```
Поддерживаются модели category, comments, genre, review, titles, users, genre_title.

Пример команды:
```
python manage.py load_from_csv -f static/data/genre.csv -m genre
```

## Примеры
>  Некоторые примеры запросов к API

GET - Получение списка всех отзывов \
**http://localhost:63342/api/v1/titles/{title_id}/reviews/**
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "score": 1,
          "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
```
PATCH - Изменение данных своей учетной записи \
**http://localhost:63342/api/v1/users/me/**

```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Создавай соцсети быстрее и проще!


# Авторы
- Сергей
- Константин
- Стив
