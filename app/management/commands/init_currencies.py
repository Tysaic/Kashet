from django.core.management.base import BaseCommand
from app.models import Currency


"""
execute: python manage.py init_currencies
"""

class Command(BaseCommand):
    help = "Init default currencies on database"

    def handle(self, *args, **kwargs):
        currencies = [
            {'name': 'Chilean Peso', 'code': 'CLP', 'symbol': '$'},
            {'name': 'US Dollar', 'code': 'USD', 'symbol': '$'},
            {'name': 'Euro', 'code': 'EUR', 'symbol': '€'},
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