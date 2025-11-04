from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as translate
from app.models import TypeTransaction


"""
execute: python manage.py init_type_transaction
"""

class Command(BaseCommand):
    help = "Init default Type Transaction on database"

    def handle(self, *args, **kwargs):
        transaction_types = [
            translate('Transferencia Bancaria'),
            translate('Efectivo'),
            translate('Orden de Pago'),
            translate('Debito/Credito'),
        ]


        for _type in transaction_types:
            obj, created = TypeTransaction.objects.get_or_create(
                name = _type
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Type Transaction "{_type}" created!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Type Transaction "{_type}" exists!'
                    )
                )