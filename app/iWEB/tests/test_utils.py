from app.models import Location
from app.models import Item
from app.models import Challenge
from app.models import UserProfile
from app.models import User


def populate_test_database():
    """
    Script to consistently populate the database with standard testing data
    Most tests use this in their setUp functions, so tests are based on this data
    """
    # Locations
    # 1 location manually setting everything except type (should autofill Fountain)
    Location.objects.create(building="Building Test (Fountain)",
                            longitude=1.22,
                            latitude=1.55555,
                            information="Test information field",
                            usable=False)
    # 1 location only setting the type
    Location.objects.create(type="BusStop")

    # Items
    # 1 item manually setting everything
    Item.objects.create(name="Test item 1",
                        description="Item test description, cost 1000",
                        price=1000)
    # 1 item only setting the name
    Item.objects.create(name="Test item 2")

    # Challenges
    # 1 challenge manually setting everything
    Challenge.objects.create(name="Test challenge 1",
                             description="Challenge test description, difficulty 3",
                             difficulty=3)
    # 1 challenge only setting the name
    Challenge.objects.create(name="Test challenge 2")

    # create some users :)
    next_username = "Test User {num}"
    for i in range(10):  # adjust range for more or less users, 10 is enough
        # don't set to less than 5 or some tests fail (intended behaviour)
        # create a user and its profile
        new_user = User.objects.create(
            username=next_username.format(num=i), password="PASSWORDTEST")
        profile = new_user.profile
        # populate with "typical" values
        profile.streak = i
        profile.score = i * 100
        if i % 2 == 0:
            profile.challenge_done = True
        profile.save()
