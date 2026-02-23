from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Django management command to seed all models with fake data.
    Usage: python manage.py seed_all <number>
    Example: python manage.py seed_all 5
    This will create 5 records for each model listed in seed_scripts.
    """
    help = 'Seed the database with initial data'

    def add_arguments(self, parser):
        """Add command line argument for number of records to create"""
        parser.add_argument('n', type=int, help='Number of entries to create for each model')

    def handle(self, *args, **kwargs):
        """
        Execute the seeding process for all models.
        Add new seed scripts to the seed_scripts list in sequence.
        """
        n = kwargs['n']

        # Import and run each seed script in sequence
        # NOTE: Add new seed files here when creating new models
        seed_scripts = [
            # Add your HR-related seed scripts here
            # Example: 'api.management.commands.seed_department',
            # Example: 'api.management.commands.seed_attendance',
        ]

        for script in seed_scripts:
            try:
                self.stdout.write(self.style.SUCCESS(f'Starting seeding for {script}...'))
                module = __import__(script, fromlist=['Command'])
                module.Command().handle(n=n)  # Pass the 'n' argument to seed script
                self.stdout.write(self.style.SUCCESS(f'Finished seeding for {script}\n'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error occurred while seeding {script}: {e}'))
