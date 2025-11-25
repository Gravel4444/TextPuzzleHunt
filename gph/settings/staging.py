from .base import *

DEBUG = True

IS_TEST = False

# Used for constructing URLs; include the protocol and trailing
# slash (e.g. 'https://galacticpuzzlehunt.com/')
DOMAIN = 'textpuzzlehunt.onrender.com'

# List of places you're serving from, e.g.
# ['galacticpuzzlehunt.com', 'gph.example.com']; or just ['*']
ALLOWED_HOSTS = ['textpuzzlehunt.onrender.com/', 'textpuzzlehunt.com', 'www.textpuzzlehunt.com']

EMAIL_SUBJECT_PREFIX = '[\u2708\u2708\u2708STAGING\u2708\u2708\u2708] '

HUNT_START_TIME = timezone.make_aware(datetime.datetime(
    year=2025,
    month=9,
    day=9,
    hour=20,
    minute=0,
))
