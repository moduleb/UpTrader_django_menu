Необходимы уставновленные Python и Django.  
Для запуска нужно выполнить команды:

```bash
git clone git@github.com:moduleb/UpTrader_django_menu.git
```
```bash
cd UpTrader_django_menu
```
```bash
python3 manage.py makemigrations
```
```bash
python3 manage.py migrate
```
```bash
python3 manage.py loaddata fixture.json
```
```bash
python3 manage.py createsuperuser
```
```bash
python3 manage.py runserver
```

Сервер доступен по адресу http://127.0.0.1:8000
