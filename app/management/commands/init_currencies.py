from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as translate
from app.models import Currency


"""
execute: python manage.py init_currencies
"""

class Command(BaseCommand):
    help = "Init default currencies on database"

    def handle(self, *args, **kwargs):
        currencies = [
            {'name': translate('Chilean Peso'), 'code': 'CLP', 'symbol': '$'},
            {'name': translate('US Dollar'), 'code': 'USD', 'symbol': '$'},
            {'name': translate('Euro'), 'code': 'EUR', 'symbol': '€'},
        ]

        for currency in currencies:
            obj, created = Currency.objects.get_or_create(
                code = currency["code"],
                name = currency["name"],
                symbol = currency["symbol"],
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Currency "{currency["name"]} created!' 
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Currency "{currency["name"]} exists!'
                    )
                )