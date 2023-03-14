from app.models import Location
from app.models import Item
from app.models import Challenge
from app.models import UserProfile
from app.models import User

def populate_test_database():
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