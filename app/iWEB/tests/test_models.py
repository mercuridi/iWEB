from django.test import TestCase
from app.models import Location
from app.models import Item
from app.models import Challenge
from app.models import UserProfile
from app.models import User
from .test_utils import populate_test_database


class test_models(TestCase):
    def setUp(self):
        populate_test_database()

    # get and test all the objects we made
    # we use a different attribute to get each just to check that's working
    def test_Location(self):
        fountain = Location.objects.get(building="Building Test (Fountain)")
        bus_stop = Location.objects.get(type="BusStop")

        # assert all the things we assigned & default field values
        self.assertEqual(fountain.type, "Fountain")
        self.assertEqual(fountain.building, "Building Test (Fountain)")
        self.assertEqual(fountain.longitude, 1.22)
        self.assertEqual(fountain.latitude, 1.55555)
        self.assertEqual(fountain.information, "Test information field")
        self.assertFalse(fountain.usable)

        self.assertEqual(bus_stop.type, "BusStop")
        self.assertTrue(bus_stop.usable)

    def test_Item(self):
        item_1 = Item.objects.get(
            description="Item test description, cost 1000")
        item_2 = Item.objects.get(name="Test item 2")

        self.assertEqual(item_1.name, "Test item 1")
        self.assertEqual(item_1.description,
                         "Item test description, cost 1000")
        self.assertEqual(item_1.price, 1000)

        self.assertEqual(item_2.name, "Test item 2")
        self.assertEqual(item_2.price, 0)

    def test_Challenge(self):
        challenge_1 = Challenge.objects.get(difficulty=3)
        challenge_2 = Challenge.objects.get(name="Test challenge 2")

        self.assertEqual(challenge_1.name, "Test challenge 1")
        self.assertEqual(challenge_1.description,
                         "Challenge test description, difficulty 3")
        self.assertEqual(challenge_1.difficulty, 3)

        self.assertEqual(challenge_2.name, "Test challenge 2")
        self.assertEqual(challenge_2.difficulty, 1)

    def test_User_and_Profile(self):
        user_1 = User.objects.get(username="Test User 1")
        user_2 = User.objects.get(username="Test User 2")
        profile_1 = user_1.profile  # pull already created profiles
        profile_2 = user_2.profile
        challenge_1 = Challenge.objects.get(pk=1)

        self.assertEqual(user_1.username, "Test User 1")
        self.assertEqual(user_2.username, "Test User 2")

        self.assertEqual(profile_1.user, user_1)
        self.assertEqual(profile_1.streak, 1)
        self.assertEqual(profile_1.points_this_week, 0)
        self.assertEqual(profile_1.current_template, "default")
        self.assertEqual(profile_1.owned_templates, "default")
        self.assertFalse(profile_1.challenge_done)
        self.assertEqual(profile_1.current_challenge, challenge_1)
