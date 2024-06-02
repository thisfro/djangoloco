# djangoloco

A simple management command to get translations from [localise.biz](https://localise.biz/) (Loco) for your django app. It will automatically download all the configured locales.

## Install
```
pip install djangoloco
```
Don't forget to enable the app
```python
INSTALLED_APPS = [
    ...
    "djangoloco",
    ...
]
```

## Setup
In your `settings.py`, set the API key from Loco (get it [here](https://localise.biz/help/developers/api-keys)) and the app that you want to translate
```python
LOCO_API_KEY = ...
LOCO_APP = "my_app"
```

## Usage
To pull the translations, run
```
python manage.py loco
```
it will create the files for the enabled languages.

Then you must run `makemessages` and `compilemessages` to actually make and compile the messages for django.