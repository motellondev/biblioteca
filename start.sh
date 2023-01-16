#!/bin/bash
python manage.py makemigrations

python manage.py migrate

python manage.py add_books

python manage.py runserver




