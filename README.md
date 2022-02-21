# Joplin Web

A Web application companion for [JoplinApp](https://joplinapp.org)

## :warning: WIP :snail:

:snail: The project is being rewritten

:ambulance: You can still get the previous version by checkouting the [vuejs branch](https://github.com/foxmask/joplin-web/tree/vuejs), but I won't maintain it anymore.

## :package: Installation

### Requirements

* :snake: Python >= 3.8
* [joplin-api](https://github.com/foxmask/joplin-api)
* :horse: [Django](https://www.djangoprojects.com)

### Installation

```python
python3 -m venv joplin-web
cd joplin-web
source bin/activate
git clone https://github.com/foxmask/joplin-web
cd joplin-web
pip install -r requirements.txt
```

##  :wrench: Settings

```bash
cd joplin_web
mv env.sample .env
```

### Set Environment Parameters

Required parameters:

|Parm | Value | Description|
|---|---|---|
|`JOPLIN_URL` | "http://127.0.0.1" | Url of Joplin webclipper service|
|`JOPLIN_PORT` |41184 | Port of Joplin webclipper service|
|`JOPLIN_WEBCLIPPER_TOKEN` | "TOBEDEFINED" | Token of Joplin webclipper service|


Optional paramenters:
* `TIME_ZONE="Asian/Seoul"`

## :dvd: Database

```
./manage.py migrate
```

## :mega: Running the Web application

```python
./manage.py runserver
October 22, 2020 - 21:06:10
Django version 3.1.2, using settings 'joplin_web.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
