from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help ="Init default all required data on database"

    def handle(self, *args, **kwargs):

        try:
            
            commands = [
                'init_departments', 'init_currencies', 
                'init_type_transaction', 'init_status_transaction',
                'init_bills_categories'
            ]
            for command in commands:
                call_command(command)
                self.stdout.write(
                    self.style.SUCCESS("Command '{}' executed successfully".format(command))
                )
        except CommandError as e:
            self.stdout.write(
                self.style.ERROR("Error in command: '{}': {}".format(command, str(e)))
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR("An unexpected error occurred: {}".format(str(e)))
            )