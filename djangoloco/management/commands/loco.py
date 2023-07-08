import os
import requests

from django.core.management.base import BaseCommand
from django.utils.translation import trans_real
from django.apps import apps
from django.conf import settings

LOCO_API_KEY = getattr(settings, 'LOCO_API_KEY', '')
API_URL = ' https://localise.biz/api/export/locale'


class Command(BaseCommand):
    help = 'Fetch translations from Loco (Localise.biz) and write them to message files'

    def handle(self, *args, **options):
        errors = 0

        if LOCO_API_KEY is None or LOCO_API_KEY == '':
            self.stdout.write(self.style.ERROR('An API key is required'))
            return

        app_config = apps.get_app_config('pflaenzli')
        app_path = app_config.path

        for locale in trans_real.get_languages():
            url = f'{API_URL}/{locale}.po'
            self.stdout.write(f'Getting translations for locale {self.style.SUCCESS(locale)}')
            response = requests.get(url, auth=(LOCO_API_KEY, ''))

            if response.status_code == 200:
                destination = f'{app_path}/locale/{locale}/LC_MESSAGES/django.po'
                self.stdout.write(f'Saving to {destination}')

                os.makedirs(os.path.dirname(destination), exist_ok=True)

                with open(destination, 'wb') as f:
                    f.write(response.content)

                self.stdout.write(self.style.SUCCESS(
                    f'Locale {locale} successfully saved to {destination}\n'))

            else:
                self.stdout.write(self.style.ERROR(
                    f'There was an error processing the request to {url}: {response.status_code}\n'))
                errors += 1

        if errors == len(trans_real.get_languages()):
            self.stdout.write(self.style.ERROR('No locales could be downloaded.'))
        elif errors > 1:
            self.stdout.write(self.style.WARNING('There were errors getting some locales.'))
        else:
            self.stdout.write(self.style.SUCCESS('All translations fetched and written to message files.'))
