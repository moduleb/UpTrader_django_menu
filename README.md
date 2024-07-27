![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![html5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![css3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)


Динамическое меню на `Django`
  + генерируется на основе базы данных.
  + можно добавлять / удалять/ перемещать пункты меню из админ панели `Django`.

---

## Запуск

>Необходимы уставновленные Python и Django.  

#### Для запуска нужно выполнить команды:

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
