# Team meeting API

API service written on DRF for managing team meeting and meeting room bookings.

## Installation using GitHub

Install PostgreSQL and create db.

```shell
git clone https://github.com/KatyaVasylieva/team-meeting-api.git
cd team-meeting-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create .env file in accordance with .env.sample.

```shell
python manage.py migrate
python manage.py runserver
```

## Run with Docker

Make sure to have Docker already installed on your computer.
Change the MEDIA_ROOT to the following one in settings:

```python
MEDIA_ROOT = "/vol/web/media"
```

```shell
docker-compose build
docker-compose up
```

## Getting access

* create user via /api/user/register
* get access token via /api/user/token


## Features

* Manage meeting room bookings
* JWT authenticated
* Admin panel in here /admin/
* Go through the documentation in here /api/doc/swagger/
* Create projects, teams
* Create meeting with or without "meeting room required"
* Filter projects, teams, meetings, bookings
* If admin user, can upload logo images to projects
