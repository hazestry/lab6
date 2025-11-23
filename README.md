API для автомобильного центра (продажа, ремонт авто) с использованием Django REST Framework.

# Требования
- Python: 3.8+
- pip: 20.0+
- Django 5.2.8
- Django REST Framework
# Установка и запуск
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/hazestry/lab6.git
   cd carcenter
   ```
2. Создайте виртуальное окружение:
   ```
   python -m venv venv
   
   # Windows
      venv\Scripts\activate

   # Linux/Mac
      source venv/bin/activate
   ```
3. Установите зависимости:
    ```
   pip install -r requirements.txt
   ```
4. Выполните миграции:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Создайте суперпользователя:
```
python manage.py createsuperuser
```
введите username, email и password.
6. Запустите сервер:
```
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`
   


