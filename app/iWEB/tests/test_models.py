from django.test import TestCase
from app.models import Location
from app.models import Item
from app.models import Challenge
from app.models import UserProfile
from app.models import User

class test_models(TestCase):
    # create some instances of each of our models
    # the creation of a user should automatically create a related user profile
    def setUp(self):
        # Locations
        # 1 location manually setting everything except type (should autofill Fountain)
        Location.objects.create(building = "Building Test (Fountain)",
                                longitude = 1.22,
                                latitude = 1.55555,
                                information = "Test information field",
                                usable = False)
        # 1 location only setting the type
        Location.objects.create(type = ('BusStop', 'BusStop'))

        # Items
        # 1 item manually setting everything
        Item.objects.create(name = "Test item 1", 
                            description = "Item test description, cost 1000",
                            price = 1000)
        # 1 item only setting the name
        Item.objects.create(name = "Test item 2")
        
        # Challenges
        # 1 challenge manually setting everything
        Challenge.objects.create(name = "Test challenge 1",
                                 description = "Challenge test description, difficulty 3",
                                 difficulty = 3)
        # 1 challenge only setting the name
        Challenge.objects.create(name = "Test challenge 2")
        
        # Users & profiles
        User.objects.create(username = "Test User 1", password = "PASSWORDTEST")
        User.objects.create(username = "Test User 2", password = "PASSWORDTEST")
        # bit messy to create and get profiles
        user_1 = User.objects.get(username = "Test User 1")
        user_2 = User.objects.get(username = "Test User 2")
        profile_1 = user_1.profile # creates a profile and fills with default values
        profile_1.streak = 5
        profile_1.score = 100
        profile_1.challenge_done = True
        profile_1.save()
        
    # get and test all the objects we made
    # we use a different attribute to get each just to check that's working
    def test_Location(self):
        fountain = Location.objects.get(building = "Building Test (Fountain)")
        bus_stop = Location.objects.get(type = "('BusStop', 'BusStop')")
        
        # assert all the things we assigned & default field values
        self.assertEqual(fountain.type, "Fountain")
        self.assertEqual(fountain.building, "Building Test (Fountain)")
        self.assertEqual(fountain.longitude, 1.22)
        self.assertEqual(fountain.latitude, 1.55555)
        self.assertEqual(fountain.information, "Test information field")
        self.assertEqual(fountain.usable, False)
        
        self.assertEqual(bus_stop.type, "('BusStop', 'BusStop')")
        self.assertEqual(bus_stop.usable, True)
        
    def test_Item(self):
        item_1 = Item.objects.get(description = "Item test description, cost 1000")
        item_2 = Item.objects.get(name = "Test item 2")
        
        self.assertEqual(item_1.name, "Test item 1")
        self.assertEqual(item_1.description, "Item test description, cost 1000")
        self.assertEqual(item_1.price, 1000)
        
        self.assertEqual(item_2.name, "Test item 2")
        self.assertEqual(item_2.price, 0)
        
    def test_Challenge(self):
        challenge_1 = Challenge.objects.get(difficulty = 3)
        challenge_2 = Challenge.objects.get(name = "Test challenge 2")
        
        self.assertEqual(challenge_1.name, "Test challenge 1")
        self.assertEqual(challenge_1.description, "Challenge test description, difficulty 3")
        self.assertEqual(challenge_1.difficulty, 3)
        
        self.assertEqual(challenge_2.name, "Test challenge 2")
        self.assertEqual(challenge_2.difficulty, 1)
        
    def test_User_and_Profile(self):
        user_1 = User.objects.get(username = "Test User 1")
        user_2 = User.objects.get(username = "Test User 2")
        profile_1 = user_1.profile  # pull already created profile
        profile_2 = user_2.profile  # should auto create a default-valued profile linked to user_2
        challenge_1 = Challenge.objects.get(pk=1)
        
        self.assertEqual(user_1.username, "Test User 1")
        self.assertEqual(user_2.username, "Test User 2")
        
        self.assertEqual(profile_1.user, user_1)
        self.assertEqual(profile_1.streak, 5)
        self.assertEqual(profile_1.score, 100)
        self.assertEqual(profile_1.current_template, "default")
        self.assertEqual(profile_1.owned_templates, "default")
        self.assertEqual(profile_1.challenge_done, True)
        self.assertEqual(profile_1.current_challenge, challenge_1)
        
        self.assertEqual(profile_2.streak, 0)
        self.assertEqual(profile_2.score, 0)
        self.assertEqual(profile_2.challenge_done, False)
        