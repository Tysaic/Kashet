from django.core.management.base import BaseCommand
from app.models import Department

"""
execute: python manage.py init_departments
"""


class Command(BaseCommand):

    help = 'Init departments on database'

    def handle(self, *args, **kwargs):
        departments = [
            {'id': 1, 'name': 'WOM'},
            {'id': 2, 'name': 'ENTEL'},
            {'id': 3, 'name': 'MOVISTAR'},
            {'id': 4, 'name': 'GALPON'},
        ]

        for dept in departments:
            ob, created = Department.objects.get_or_create(
                id = dept['id'],
                defaults = {'name': dept['name']}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'DEPARTMENT "{dept["name"]}" created!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'DEPARTMENT "{dept["name"]}" exists!')
                )