from django.core.management.base import BaseCommand
from api.AttendanceStatus.model import AttendanceStatus


class Command(BaseCommand):
    help = 'Seed AttendanceStatus with present, absent, halfday'

    def handle(self, *args, **kwargs):
        statuses = ['present', 'absent', 'halfday']
        for s in statuses:
            _, created = AttendanceStatus.objects.get_or_create(status=s)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {s}'))
            else:
                self.stdout.write(f'Already exists: {s}')

# run with:
# python manage.py seed_attendance_status