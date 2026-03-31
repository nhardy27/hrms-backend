from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.Attendance.model import Attendance
from api.AttendanceStatus.model import AttendanceStatus
from datetime import date, time
import random


class Command(BaseCommand):
    """
    Seed attendance for all employees for given dates with random times.
    Usage: python manage.py seed_attendance 2025-06-01 2025-06-30
    Dates can be a range (start end) or individual dates.
    """
    help = 'Seed attendance for all employees for given dates'

    def add_arguments(self, parser):
        parser.add_argument('dates', nargs='+', type=str, help='Dates in YYYY-MM-DD format (start end for range, or individual dates)')

    def handle(self, *args, **kwargs):
        raw_dates = kwargs['dates']

        # If 2 dates given, treat as range
        if len(raw_dates) == 2:
            from datetime import timedelta
            start = date.fromisoformat(raw_dates[0])
            end = date.fromisoformat(raw_dates[1])
            delta = (end - start).days + 1
            dates = [start + timedelta(days=i) for i in range(delta)]
        else:
            dates = [date.fromisoformat(d) for d in raw_dates]

        users = User.objects.filter(is_active=True)
        statuses = {s.status: s for s in AttendanceStatus.objects.all()}

        if not statuses:
            self.stdout.write(self.style.ERROR('No AttendanceStatus records found. Seed them first.'))
            return

        created = 0
        skipped = 0

        for user in users:
            for d in dates:
                # Skip weekends (Saturday=5, Sunday=6)
                if d.weekday() in (5, 6):
                    continue

                # Random status weights: 80% present, 10% halfday, 10% absent
                status_key = random.choices(
                    ['present', 'halfday', 'absent'],
                    weights=[80, 10, 10]
                )[0]
                status = statuses.get(status_key)
                if not status:
                    continue

                check_in = check_out = None

                if status_key == 'present':
                    check_in = time(random.randint(8, 10), random.randint(0, 59))
                    check_out = time(random.randint(17, 19), random.randint(0, 59))
                elif status_key == 'halfday':
                    check_in = time(random.randint(8, 10), random.randint(0, 59))
                    check_out = time(random.randint(12, 14), random.randint(0, 59))

                _, created_flag = Attendance.objects.get_or_create(
                    user=user,
                    date=d,
                    defaults={
                        'attendance_status': status,
                        'check_in': check_in,
                        'check_out': check_out,
                    }
                )
                if created_flag:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(f'Done! Created: {created}, Skipped (already exist): {skipped}'))


# run with:
# python manage.py seed_attendance 2026-03-02 2026-03-31