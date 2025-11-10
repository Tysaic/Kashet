from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as translate
from app.models import CategoryBill


"""
execute: python manage.py init_bills_categories
"""

class Command(BaseCommand):
    help = "Init default Bills Categories on database"

    def handle(self, *args, **kwargs):
        categories = [
            (translate("Servicio"), translate("Gastos relacionados con servicios como electricidad, agua, internet, etc.")),
            (translate("Suministro"), translate("Gastos en materiales y suministros necesarios para las operaciones diarias.")),
            (translate("Personal"), translate("Gastos asociados al personal, incluyendo salarios, beneficios y formación.")),
            (translate("Mantenimiento"), translate("Gastos para el mantenimiento y reparación de equipos e instalaciones.")),
            (translate("Marketing"), translate("Gastos relacionados con publicidad, promociones y actividades de marketing.")),
            (translate("Viajes"), translate("Gastos de transporte, alojamiento y dietas durante viajes de negocios.")),
            (translate("Tecnología"), translate("Gastos en software, hardware y servicios tecnológicos.")),
            (translate("Consultoría"), translate("Gastos en servicios de consultoría externa y asesoramiento profesional.")),
            (translate("Impuesto"), translate("Gastos relacionados con impuestos y tasas gubernamentales.")),
            (translate("Otros"), translate("Cualquier otro gasto que no encaje en las categorías anteriores.")),
        ]


        for name, description in categories:
            obj, created = CategoryBill.objects.get_or_create(
                name = name,
                description = description
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Category name: "{name}" created!'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Category Name "{name}" exists!'
                    )
                )