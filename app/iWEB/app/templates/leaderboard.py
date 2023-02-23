from leaderboard.leaderboard import Leaderboard
from django.contrib.auth.models import User

userList = User.objects.values()

#create new leaderboard
highscore_lb = Leaderboard('highscores')

#defining options
DEFAULT_PAGE_SIZE = 25
DEFAULT_REDIS_HOST = 'localhost'
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 0
DEFAULT_MEMBER_DATA_NAMESPACE = 'member_data'
DEFAULT_GLOBAL_MEMBER_DATA = False
ASC = 'asc'
DESC = 'desc'
MEMBER_KEY = 'member'
MEMBER_DATA_KEY = 'member_data'
SCORE_KEY = 'score'
RANK_KEY = 'rank'

#ranking members
def getLeaders():
  return userList
#add members using rank_member
for index in range(1, 6):
  highscore_lb.rank_member('member_%s' % index, index)

#retrieve ranks 1 to 5
highscore_lb.members_from_rank_range(1, 5)

#retrieve user rank
highscore_lb.around_me("")