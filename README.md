Проект Yamdb API позволяет пользователям публиковать Отзывы.

Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Каждый ресурс описан в документации: указаны роуты (адреса, по которым можно сделать запрос),
разрешённые типы запросов, права доступа и дополнительные параметры.

### Стек применяемых технологий:
- __Python__, 
- __Django rest framework__, 
- __JWT__


### Доступные роуты для взаимодействия у _НЕ аутентифицированных_ пользователей (безопасные запросы CRUD):
- api/v1/auth/signup/ - Регистрация пользователя;
- api/v1/auth/token/ - Получение токена по "Username" и коду подтверждения с почты;
- api/v1/titles/{title_id}/reviews/ - Просмотр отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Просмотр комментариев;
...

### Дополнительные роуты для взаимодействия у _аутентифицированных_ пользователей с учетом их ролей:
_"User"_

- api/v1/users/me/ - Получение данных своей учетной записи/Изменение данных своей учетной записи;
- api/v1/titles/{title_id}/reviews/ - Просмотр/добавление отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/ - Редактирование/удаление/ получение по id отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Просмотр/добавление комментариев;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - Редактирование/удаление/ получение по id комментариев;
  
_"Moderator"_

- api/v1/users/me/ - Получение данных своей учетной записи/Изменение данных своей учетной записи;
- api/v1/titles/{title_id}/reviews/ - Просмотр/добавление отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/ - Редактирование/удаление/ получение по id отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Просмотр/добавление комментариев;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - Редактирование/удаление/ получение по id комментариев;

_"Admin"_

- api/v1/users/ - Получение списка всех пользователей/Добавление пользователя;
- api/v1/users/{username}/ - Получение пользователя/Внесение изменений пользователя/Удаление пользователя;
- api/v1/users/me/ - Получение данных своей учетной записи/Изменение данных своей учетной записи;
- api/v1/titles/{title_id}/reviews/ - Просмотр/добавление отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/ - Редактирование/удаление/ получение по id отзывов;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Просмотр/добавление комментариев;
- api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - Редактирование/удаление/ получение по id комментариев;

### Примеры запросов:
- POST-запрос на регистрацию пользователя:
#### POST ...api/v1/auth/signup/ 
Пример ответа:

    {
    "email": "user@example.com",
    "username": "user"
    }

- POST-запрос на добавления жанра или произведения:
### POST ...api/v1/categories(genres)/ | ...api/v1/genres/
Тело запроса:

    {
    "name": "string",
    "slug": "^-$"
    }

- POST-запрос на добавления произведения:
### POST ...api/v1/titles/
Тело запроса:

    {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
    "string"
    ],
    "category": "string"
    }

- POST-запрос на получение токена по "Username" и коду подтверждения с почты.
#### POST .../api/v1/posts/14/comments/
Тело запроса:

    {
    "username": "user",
    "confirmation_code": "confirmation_code"
    } 
Пример ответа:

    {
    "token": "string"
    } 

- GET-запрос Получить список всех отзывов.
#### GET ...api/v1/titles/{title_id}/reviews/
Получение списка всех отзывов:
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
#### GET ...api/v1/titles/{title_id}/reviews/{review_id}/comments/
Получение списка всех комментариев:
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
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
  }
```
...

## Для локального развертывания проекта у себя, необходимо:

1.  Клонировать проект с GitHub.com примени следующую команду в терминале: <br>`git clone git@github.com:MaksimGolovkin/api_yamdb.git`

2. Настроить виртуальное окружение в Вашей IDE.
    <br>`python -m venv venv`
    <br>`source venv/Scripts/activate`

3. Установить зависимости из файла 'requirements.txt' с помощью команды: <br>`pip install -r requirements.txt`

4. Создайте миграции в проекте из папки (где находится файл 'manage.py') проекта, с помощью команды:
    <br>`python manage.py makemigrations`

5. Примените миграции в проекте из папки (где находится файл 'manage.py') проекта, с помощью команды:
    <br>`python manage.py migrate`

6. Запустить проект из папки (где находится файл 'manage.py') проекта, с помощью команды:
    <br>`python manage.py runserver`

7. Перейти по ссылке в любом из имеющихся браузеров, добавив вместо "(...)" любой из имеющихся роутов: 
    <br>`http://127.0.0.1:8000/(...)`

- Для того, чтобы наполнить базу данных с помощью CSV файлов, вы можете использовать скрипт, для этого необходимо выполнить команду: 
`python manage.py import_data`


### _Дополнительная информацию по работе проекта, содержится по адерсу:_
_<br>`http://127.0.0.1:8000/redoc/`_

---
_Авторы проекта - sairin-mihail102, Egor-Koba, maksimgolovkin96. :)_
