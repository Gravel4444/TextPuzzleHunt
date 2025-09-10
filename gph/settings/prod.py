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
ALLOWED_HOSTS = ['textpuzzlehunt.onrender.com']


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === 미들웨어 설정 (가장 중요한 수정) ===
# base.py의 MIDDLEWARE 리스트에 Whitenoise 미들웨어를 추가합니다.
# 'SecurityMiddleware' 바로 다음에 위치시키는 것이 가장 안정적입니다.
MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
    'whitenoise.middleware.WhiteNoiseMiddleware'
)

RECAPTCHA_SCORE_THRESHOLD = 0.5

# Google Analytics
GA_CODE = '''
<script>
  /* FIXME */
</script>
'''
