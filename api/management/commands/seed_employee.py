from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.Employee.model import Employee
from api.Department.model import Department
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed Employee data'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of employees to create')

    def handle(self, *args, **kwargs):
        n = kwargs['n']
        fake = Faker()

        if not Department.objects.exists():
            for dept in ['HR', 'IT', 'Finance']:
                Department.objects.create(name=dept)

        departments = list(Department.objects.all())
        designations = ['Manager', 'Developer', 'Analyst']
        roles = ['admin', 'employee']

        for i in range(n):
            user = User.objects.create_user(
                username=f"{fake.user_name()}{i}",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password123'
            )

            role = 'admin' if i == 0 else random.choice(roles)  # First user is admin
            
            Employee.objects.create(
                user=user,
                phone=fake.phone_number()[:15],
                designation=random.choice(designations),
                department=random.choice(departments),
                role=role,
                date_of_joining=fake.date_between(start_date='-1y', end_date='today')
            )

        self.stdout.write(self.style.SUCCESS(f'Created {n} employees (1 admin, {n-1} employees)'))