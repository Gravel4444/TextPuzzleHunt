# gph/formats/ko/formats.py

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

# Django에서 사용할 한국어 날짜 및 시간 형식입니다.
# https://docs.djangoproject.com/en/stable/ref/templates/builtins/#date

# 예시: 2025년 9월
YEAR_MONTH_FORMAT = 'Y년 n월'

# 예시: 9월 7일
MONTH_DAY_FORMAT = 'n월 j일'

# 예시: 2025.09.07
SHORT_DATE_FORMAT = 'Y.m.d'

# 예시: 2025.09.07 오후 3:10
SHORT_DATETIME_FORMAT = 'Y.m.d A g:i'

# 예시: 2025년 9월 7일 (일)
DATE_WITH_DAY_FORMAT = 'Y년 n월 j일 (D)'

# 예시: 2025년 9월 7일 (일) 오후 3:10
DATETIME_WITH_DAY_FORMAT = 'Y년 n월 j일 (D) A g:i'

# gph-site에서 자주 사용하는 사용자 정의 형식들
DATE_FORMAT = 'Y년 n월 j일'
TIME_FORMAT = 'A g:i'
DATETIME_FORMAT = 'Y년 n월 j일 A g:i'
YEAR_FORMAT = 'Y'
# 가장 많이 사용될 형식
DATE_AT_TIME_FORMAT = 'Y.m.d. H:i'