from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Workouts
        run = Workout.objects.create(name='Running', description='Run fast!', difficulty='Medium')
        lift = Workout.objects.create(name='Weight Lifting', description='Lift heavy!', difficulty='Hard')
        yoga = Workout.objects.create(name='Yoga', description='Stretch and relax', difficulty='Easy')

        # Create Users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User(name='Batman', email='batman@dc.com', team=dc),
        ]
        for user in users:
            user.save()

        # Create Activities
        Activity.objects.create(user=users[0], workout=run, date=date.today(), duration_minutes=30, points=50)
        Activity.objects.create(user=users[1], workout=lift, date=date.today(), duration_minutes=45, points=70)
        Activity.objects.create(user=users[2], workout=yoga, date=date.today(), duration_minutes=60, points=40)
        Activity.objects.create(user=users[3], workout=run, date=date.today(), duration_minutes=25, points=45)

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, total_points=120)
        Leaderboard.objects.create(team=dc, total_points=85)

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
