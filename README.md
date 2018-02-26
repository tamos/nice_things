# We Can Have Nice Things Repository

Repository for CAPP 30122 Winter 2018 Project

  * Alexander Tyan
  * Kevin Sun
  * Tyler Amos
  
  
To Set Up The App:

## 1. Install PostgreSQL


## 2. Create a PostgrSQL User nice_things

#### On Mac/Linux

  ``` sudo -u postgres psql ```
  
  ```CREATE USSER nice_things LOGIN password 'uccs'; ```
  
  ```CREATE DATABASE nice_things_db OWNER nice_things;```
  
  Leave PostgresSQL running and now, in terminal:
  
  ```python3 manage.py makemigrations```
  
  ```python3 manage.py migrate```
  
  ```python3 update_db.py update_food_table```
  
  ```python3 update_db.py update_wages_table```
  
  ```python3 manage.py runserver```