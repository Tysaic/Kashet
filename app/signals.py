import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from app.models import BudgetFile

@receiver(post_delete, sender=BudgetFile)
def delete_file_from_storage(sender, instance, **kwargs):

    if instance.file and os.path.isfile(instance.file.path):
        path_to_delete = instance.file.path
        folder_path_to_delete = os.path.dirname(path_to_delete)

        try:
            os.remove(instance.file.path)

            if not os.listdir(folder_path_to_delete):
                #Folder is empty?
                os.rmdir(folder_path_to_delete)

        except Exception as e:
            print(f"No se pudo eliminar el archivo fisico por: {e}")
