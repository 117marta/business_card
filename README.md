# business_card
Recruitment task

## Table of Contents
* [General info](#general-info)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)


## General info
This project was made as a recruitment task.


## Technologies Used
* Project was created with:
* Django==4.1
* django-formtools==2.5.1
* mysql-connector-python==9.1.0
* pillow==11.1.0
* pre_commit==4.0.1
* pytest-django==4.9.0
* qrcode==8.0
* requests==2.32.3
* responses==0.25.6


## Features
* Registration and Login
* Fill data to create a business card
* Generate a QR code
* Create a multistep form to leave your data. Send this data by API
* Display a random mem


## Setup
Project requirements are in _requirements.txt_. <br>
To get started:
* `sudo apt install mysql-server`
* `pip install -r requirements.txt`
* `python manage.py migrate`
* `python manage.py runserver`


## Usage
* After you clone this repo to your desktop, go to its root directory and run `pip install -r requirements.txt`
to install its dependencies
* When the dependencies are installed, run migrations `python manage.py migrate` and run server
`python manage.py runserver` to start application
* You will be able to access it at `http://127.0.0.1:8000/home-page/`


## Project Status
Backend is _complete_.<br>


## Contact
Created by _117marta_ - feel free to contact me!
