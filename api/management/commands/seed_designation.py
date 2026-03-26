from django.core.management.base import BaseCommand
from faker import Faker
from api.Department.model import Department
from api.Designation.model import Designation

fake = Faker()

DESIGNATIONS = ['Manager', 'Senior Engineer', 'Junior Engineer', 'Analyst', 'Team Lead', 'Intern', 'Consultant']

class Command(BaseCommand):
    help = 'Seed Designation data'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)

    def handle(self, *args, **kwargs):
        n = kwargs['n']
        departments = list(Department.objects.all())
        if not departments:
            self.stdout.write(self.style.WARNING('No departments found. Seed departments first.'))
            return

        created = 0
        for dept in departments:
            for title in DESIGNATIONS[:n]:
                _, was_created = Designation.objects.get_or_create(name=title, department=dept)
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} designations.'))
