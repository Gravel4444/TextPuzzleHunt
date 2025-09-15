# gunicorn.py - Render 운영 서버용

import os

# Render가 제공하는 PORT 환경 변수를 사용해 서버를 외부에 개방합니다.
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Render의 CPU 사양에 맞춰 워커 수를 2-4개 정도로 고정하는 것이 안정적입니다.
workers = 3

# Django Channels를 사용하므로 ASGI 워커 클래스를 유지합니다.
worker_class = 'uvicorn.workers.UvicornWorker'

# Gunicorn의 시작/종료 같은 정보를 확인하기 위해 'info'로 설정하는 것이 좋습니다.
loglevel = 'info'

# -- 제거된 옵션 --
# pidfile = 'gunicorn.pid' # Render 환경에서는 불필요합니다.
# reload = True # 운영 환경에서는 반드시 False여야 하므로 옵션을 제거합니다.