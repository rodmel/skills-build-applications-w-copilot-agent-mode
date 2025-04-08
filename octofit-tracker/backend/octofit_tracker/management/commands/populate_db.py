import logging
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        logging.debug('Connecting to MongoDB...')
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        logging.debug('Dropping existing collections...')
        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        logging.debug('Creating users...')
        # Create users
        users = [
            User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
            User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
            User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
            User(_id=ObjectId(), username='crashoverride', email='crashoverride@mhigh.edu', password='crashoverridepassword'),
            User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users)
        logging.debug('Users created successfully.')

        logging.debug('Creating teams...')
        # Create teams
        team1 = Team(_id=ObjectId(), name='Blue Team')
        team2 = Team(_id=ObjectId(), name='Gold Team')
        team1.save()
        team2.save()
        for user in users:
            team1.members.add(user)
        logging.debug('Teams created successfully.')

        logging.debug('Creating activities...')
        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)
        logging.debug('Activities created successfully.')

        logging.debug('Creating leaderboard entries...')
        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=100),
            Leaderboard(_id=ObjectId(), user=users[1], score=90),
            Leaderboard(_id=ObjectId(), user=users[2], score=95),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)
        logging.debug('Leaderboard entries created successfully.')

        logging.debug('Creating workouts...')
        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)
        logging.debug('Workouts created successfully.')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
