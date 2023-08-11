## Introduction
Chat application named Conversat developed for the purpose of smooth group and personal conversation.

## Features


- Realtime Personal chats
- Realtime group chats
- Create groups
- Notification system
- Send friend requests
- Realtime text messages
- Realtime audio, video messages
- Realtime images, documents uploading

## Tech Stack

**Client Side:** HTML, CSS, SCSS, TailwindCSS, JavaScript, JQuery

**Server Side:** Python, Django, Django Channels, Websockets, Redis

**Database:** SQLite (can be upgraded to MySQL/Postgress)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Django settings

`DEBUG = TRUE`

`SECRET_KEY = "django-insecure-1cih0ds(h2(w4c)gy8+v1ihj=g-2-0d0^%xw+19s#x%mo6a0*%"`



## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/ChatApplication

```
or simply download this project from https://github.com/Mr-Atanu-Roy/ChatApplication

In project directory Create a virtual environment of any name(say env)

```bash
  virtualenv env

```
Activate the virtual environment

For windows:
```bash
  env\Script\activate

```
Install dependencies
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands
```bash
  py manage.py makemigrations
  py manage.py migrate

```

Create a super user
```bash
  py manage.py createsuperuser

```


To run the project in your localserver
```bash
  py manage.py runserver

```
## Authors

- [@Atanu Roy](https://github.com/Mr-Atanu-Roy)

