from .base import *
import dj_database_url
import os

DEBUG = False
IS_TEST = False

ssl_require=True

# Used for constructing URLs; include the protocol and trailing
# slash (e.g. 'https://galacticpuzzlehunt.com/')
DOMAIN = 'FIXME'

# List of places you're serving from, e.g.
# ['galacticpuzzlehunt.com', 'gph.example.com']; or just ['*']
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=False)
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

# if 'MIDDLEWARE' in locals():
#     MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


RECAPTCHA_SCORE_THRESHOLD = 0.5

# Google Analytics
GA_CODE = '''
<script>
  /* FIXME */
</script>
'''
