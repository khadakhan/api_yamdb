# Rest API DRF
Python API на Django Rest Framework.

Проект позволяет разработчикам интегрировать API 
**социальной сети формата IMDb** через стандартные HTTP-запросы в свои приложения, веб-сайты или другие сервисы.


> [!NOTE]
> С помощью API можно делать аутентификацию, создавать, обновлять, удалять пользователей, произведения, категории, жанры произведений, отзывы на произведения, а также комментарии к отзывам.
## Документация:
> [!TIP]
> http://127.0.0.1:8000/redoc/ - можно перейти для просмотра подробной документации по API.
(доступна после активации сервера Django)


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
