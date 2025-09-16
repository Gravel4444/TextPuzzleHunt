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
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
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
<script async src="https://www.googletagmanager.com/gtag/js?id=G-20GVWJS0Q8"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-20GVWJS0Q8');
</script>
'''

# csrf 403 에러 수정.
# Render 배포 환경의 CSRF 보안 설정을 위해 웹사이트의 주소를 신뢰할 수 있는 출처로 추가합니다.
CSRF_TRUSTED_ORIGINS = ['https://textpuzzlehunt.onrender.com']


# Discord Webhook URLs
ALERT_WEBHOOK_URL = os.environ.get('ALERT_WEBHOOK_URL')
SUBMISSION_WEBHOOK_URL = os.environ.get('SUBMISSION_WEBHOOK_URL')
FREE_ANSWER_WEBHOOK_URL = os.environ.get('FREE_ANSWER_WEBHOOK_URL')
VICTORY_WEBHOOK_URL = os.environ.get('VICTORY_WEBHOOK_URL')

# Discord Bot Credentials
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.environ.get('DISCORD_GUILD_ID')
DISCORD_HINT_CHANNEL_ID = os.environ.get('DISCORD_HINT_CHANNEL_ID')
