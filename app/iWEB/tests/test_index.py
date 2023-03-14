from django.test import TestCase
from django.test import Client
from app.models import Location
from app.models import User
from app.models import UserProfile
from app.index import get_leaderboard
from app.index import get_locations
from .test_utils import populate_test_database

client = Client()

class test_index(TestCase):
    def setUp(self):
        populate_test_database()
    
    def test_leaderboard(self):
        # get leaderboards with different sizes
        num_users = User.objects.all().count()
        if num_users < 5:
            self.fail(f"Not enough users ({num_users}, 5 required) to test leaderboard")
        else:
            leaderboard_default = get_leaderboard()             # relies on the default arg
            leaderboard_negative = get_leaderboard(-1)          # edge case of asking for negative values
            leaderboard_1 = get_leaderboard(1)                  # single person leaderboard
            leaderboard_5 = get_leaderboard(5)                  # 5 people leaderboard
            leaderboard_toobig = get_leaderboard(num_users+1)   # leaderboard with more users than exist
            
            # check lengths are the same as we expect them to be
            self.assertEqual(len(leaderboard_1), 1)
            self.assertEqual(len(leaderboard_negative), 1)
            self.assertEqual(len(leaderboard_5), 5)
            self.assertEqual(len(leaderboard_toobig), num_users)
            
            # check the highest ranked user is the same for all leaderboards
            self.assertEqual(leaderboard_default[0], leaderboard_negative[0])
            self.assertEqual(leaderboard_negative[0], leaderboard_1[0])
            self.assertEqual(leaderboard_1[0], leaderboard_5[0])
            self.assertEqual(leaderboard_5[0], leaderboard_toobig[0])
            
            # check that every profile exists and matches the one we expect it to
            # when we create a leaderboard for all of them
            # can't be a direct "==" comparison as we add the "username" field to leaderboards
            profiles = UserProfile.objects.values().order_by("-score")
            i = 0
            for profile in profiles:
                self.assertDictContainsSubset(profile, leaderboard_toobig[i])
                i += 1
        
    def test_locations(self):
        # get locations
        all_locations = get_locations()
        fountains = all_locations["Fountains"]
        bus_stops = all_locations["Bus stops"]
        bins = all_locations["Bins"]
        
        # get amounts of locations
        num_fountains = len(fountains)
        num_bus_stops = len(bus_stops)
        num_bins = len(bins)
        num_locations = num_fountains + num_bus_stops + num_bins

        self.assertEqual(num_locations, Location.objects.all().count())