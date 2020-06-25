### Программа для проведения опросов пользователей

Программа реализованная с помощью Django REST Framework, 
в качестве результата генерирует JSON совместимые ответы.

## Установка

Для корректной работы необходим python 3.6+

1. Для установки необходимо склонировать репозиторий:
`git clone URL_repository`
2. Создать виртуальное окружение:
`python -m venv venv`
3. Активировать окружение. В зависимости от системы:
    * windows: `.\venv\scripts\activate.bat`
    * nix: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements`
5. Зарегистрировать супер-пользователя Django:
`python manage.py createsuperuser --username=USERNAME`
6. Создать миграции для БД: `python manage.py makemigrations`
7. Импортировать миграции в БД: `python manage.py migrate`
8. Запустить Django сервер: `python manage.py runserver`

## Описание API для опросов

Краткое руководство по использованию API для опросов.

_В текущей редакции в API отсутствует валидация ответов пользователей._

### Запросы выполняющиеся без авторизации

Запросы предназначеные для пользователей сервиса.

* Показать актуальные опросы: `GET /user-answers/active`
* Показать информацию о конкретном опросе: `GET /user-answers/active-polls/<int:poll_id>`  
* Показать ответы пользователя: `GET /user-answer/<int:user_poll_id>`
* Отправить ответы на опрос: `POST /user-answers/active-polls/<int:poll_id>`
 
Отправлять необходимо ответ сразу на все вопросы опроса, иначе система генерирует ошибку с кодом 400. 
Ожидаемый формат ответа на опрос:
 
```
{
    "user_poll_id":42,
    "answers":[
        {
            "question":2,
            "answer":"yes"
        },
        { 
            "question":3,
            "answer":"no"
        },
        { 
            "question":4,
            "answer":"may be"} 
    ]
}
```

### Запросы требущие авторизации

Запросы предназначенные для администрации сервиса.

* Показать все существующие опросы: `GET /polls/`
* Создать новый опрос: `POST /polls/`
* Редактировать опрос: `PUT /polls/<int:poll_id>/`
* Удалить опрос: `DELETE /polls/<int:poll_id>/`
* Показать вопросы из опроса: `GET /polls/<int:poll_id>/questions/`
* Добавить вопрос к опросу: `POST /polls/<int:poll_id>/questions/`
* Показать конкретный вопрос: `GET /questions/<int:question_id>/`
* Редактировать вопрос: `PUT /questions/<int:question_id>/`
* Удалить вопрос: `DELETE /questions/<int:question_id>/`
* Варианты ответа для закрытого вопроса: `GET /questions/<int:question_id>/variants/`
* Показать конкретный вариант: `GET /variants/<int:variant_id>/`
* Редактировать вариант ответа: `PUT /variants/<int:varian_id>/`
* Удалить вариант ответа: `DELETE /variants/<int:variant_id>/`
