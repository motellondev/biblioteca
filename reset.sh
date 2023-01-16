#!/bin/bash

# MAIN APP

if [ -d ./webapp/management/__pycache__ ];
then
rm -r ./webapp/management/__pycache__
fi

if [ -d ./webapp/__pycache__ ];
then
rm -r ./webapp/__pycache__
fi

if [ -d ./webapp/migrations/__pycache__ ];
then
rm -r ./webapp/migrations/__pycache__
fi

if [ -d ./webapp/management/commands/__pycache__ ];
then
rm -r ./webapp/management/commands/__pycache__
fi

if [ -f ./webapp/migrations/0001_initial.py ];
then
rm ./webapp/migrations/0001_initial.py
fi



# PROJECT FOLDER

if [ -d ./Biblioteca/__pycache__ ];
then
rm -r ./Biblioteca/__pycache__
fi


if [ -f ./db.sqlite3 ];
then
rm -r ./db.sqlite3
fi


