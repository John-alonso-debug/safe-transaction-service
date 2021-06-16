import sys

from django.apps import AppConfig


class HistoryConfig(AppConfig):
    name = 'history'
    verbose_name = 'Safe Transaction Service'

    def ready(self):
        from . import signals  # noqa

        for argument in sys.argv:
            if 'gunicorn' in argument:
                # Just run this on production
                # TODO Find a better way
                from contracts.tx_decoder import get_db_tx_decoder
                get_db_tx_decoder()  # Build tx decoder cache
                break
