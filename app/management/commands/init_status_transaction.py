from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as translate
from app.models import StatusTransaction


"""
execute: python manage.py init_status_transaction
"""

class Command(BaseCommand):
    help = "Init default Type Transaction on database"

    def handle(self, *args, **kwargs):
        status_types = [
            (translate('En Proceso'), False),
            (translate('Aprobado'), True),
            (translate('En espera'), False),
            (translate('Rechazado'), True)
        ]


        for name_status, able in status_types:
            obj, created = StatusTransaction.objects.get_or_create(
                name = name_status,
                enable = able
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Status Transaction "{name_status}" created!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Status Transaction "{name_status}" exists!'
                    )
                )