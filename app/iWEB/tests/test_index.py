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
            self.fail(
                f"Not enough users in test database ({num_users}, 5 required) to test leaderboard")
        else:
            # relies on the default arg
            leaderboard_default = get_leaderboard()
            # edge case of asking for negative values
            leaderboard_negative = get_leaderboard(-1)
            # single person leaderboard
            leaderboard_1 = get_leaderboard(1)
            # 5 people leaderboard
            leaderboard_5 = get_leaderboard(5)
            # leaderboard with more users than exist
            leaderboard_toobig = get_leaderboard(num_users+1)
            # leaderboard with a length of 0
            leaderboard_0 = get_leaderboard(0)

            # check lengths are the same as we expect them to be
            self.assertEqual(len(leaderboard_1), 1)
            self.assertEqual(len(leaderboard_negative), 1)
            self.assertEqual(len(leaderboard_5), 5)
            self.assertEqual(len(leaderboard_toobig), num_users)
            self.assertEqual(len(leaderboard_0), 0)

            # check the highest ranked user is the same for all leaderboards
            self.assertEqual(leaderboard_default[0], leaderboard_negative[0])
            self.assertEqual(leaderboard_negative[0], leaderboard_1[0])
            self.assertEqual(leaderboard_1[0], leaderboard_5[0])
            self.assertEqual(leaderboard_5[0], leaderboard_toobig[0])

            # check that every profile exists and matches the one we expect it to
            # when we create a leaderboard for all of them
            # can't be a direct "==" comparison as we add the "username" field to leaderboards
            profiles = UserProfile.objects.values().order_by("-points_this_week")
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

        if num_fountains < 1:
            self.fail("No fountains pulled from database.")
        else:
            # check we've got the right amount from our database queries
            self.assertEqual(num_fountains, Location.objects.filter(type = "Fountain").count())
            self.assertEqual(num_bus_stops, Location.objects.filter(type = "BusStop").count())
            self.assertEqual(num_bins, Location.objects.filter(type = "Bin").count())
            self.assertEqual(num_locations, Location.objects.all().count())
            
            # check that the fountains we've got matches with the one we expect it to in the database
            # we check the first and the last entries in the fountains list (can be the same if only 1 entry)
            database_fountain_first = Location.objects.get(building=fountains[0][2])
            database_fountain_last = Location.objects.get(building=fountains[-1][2])
            # check some different attributes are equal
            self.assertEqual(database_fountain_first.longitude,     fountains[0][1])
            self.assertEqual(database_fountain_first.information,   fountains[0][3])
            self.assertEqual(database_fountain_last.latitude,       fountains[-1][0])
            self.assertEqual(database_fountain_last.information,    fountains[-1][3])
            
    def test_points_increment(self):
        pass
