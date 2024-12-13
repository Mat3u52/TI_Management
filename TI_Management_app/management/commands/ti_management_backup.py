from django.core.management.base import BaseCommand
from TI_Management.cron import ti_management_backup  # Import your function

class Command(BaseCommand):
    help = "Runs the TI management backup process"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting backup...")
        ti_management_backup()  # Call your existing function
        self.stdout.write("Backup completed successfully.")
