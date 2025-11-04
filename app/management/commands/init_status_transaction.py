from django.core.management.base import BaseCommand
from app.models import StatusTransaction


"""
execute: python manage.py init_status_transaction
"""

class Command(BaseCommand):
    help = "Init default Type Transaction on database"

    def handle(self, *args, **kwargs):
        status_types = [
            'Aprobado',
            'En espera',
            'Rechazado',
        ]


        for name_status in status_types:
            obj, created = StatusTransaction.objects.get_or_create(
                name = name_status
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