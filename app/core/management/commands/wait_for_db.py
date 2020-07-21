import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until it can connect to database."""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_connection = None
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('Database not ready yet, '
                                  'trying again after 1s...')
                time.sleep(1)
        # Success!
        self.stdout.write(self.style.SUCCESS('Database available!'))
