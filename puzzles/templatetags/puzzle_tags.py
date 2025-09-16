import hashlib
import markdown
import os
import re

from django import template
from django.template.base import NodeList
from django.template.loader import render_to_string #추가함
from django.template.loader_tags import BlockNode
from django.urls import reverse #추가함
from django.utils import timezone
from django.utils import formats
from django.utils import dateformat #추가함
from django.utils.translation import gettext as _
from django.utils.html import strip_spaces_between_tags
from django.utils.safestring import mark_safe

register = template.Library()

# 시간 차이 계산
@register.simple_tag
def format_duration(secs):
    if secs is None:
        return ''
    
    secs = max(int(secs), 0)

    # 평균적인 시간 단위를 초로 정의 (윤년 등 고려)
    SECONDS_IN_DAY = 86400
    SECONDS_IN_YEAR = 31557600  # 365.25 days
    SECONDS_IN_MONTH = 2629800   # year / 12

    years = secs // SECONDS_IN_YEAR
    secs %= SECONDS_IN_YEAR

    months = secs // SECONDS_IN_MONTH
    secs %= SECONDS_IN_MONTH

    days = secs // SECONDS_IN_DAY
    secs %= SECONDS_IN_DAY
    
    hours = secs // 3600
    secs %= 3600
    
    mins = secs // 60
    
    # 가장 큰 두 개의 시간 단위로 표시
    if years > 0:
        return _('{}년 {}개월').format(int(years), int(months))
    elif months > 0:
        return _('{}개월 {}일').format(int(months), int(days))
    elif days > 0:
        return _('{}일 {}시간').format(int(days), int(hours))
    elif hours > 0:
        return _('{}h{}m').format(int(hours), int(mins))
    elif mins > 0:
        # 분 단위에서는 초를 표시하기 위해 나머지 초 계산
        final_secs = secs % 60
        return _('{}m{}s').format(int(mins), int(final_secs))
    else:
        return _('{}s').format(int(secs))

@register.simple_tag
def format_time_since(timestamp, now):
    text = format_duration((now - timestamp).total_seconds())
    return mark_safe('<time datetime="%s" data-format="%s">%s</time>'
        % (timestamp.isoformat(), formats.get_format('DATE_AT_TIME'), text))

@register.simple_tag
def days_between(before, after):
    return round((after - before).total_seconds() / 60 / 60 / 24, 1)

@register.filter
def unix_time(timestamp):
    return timestamp.timestamp() if timestamp else ''

@register.simple_tag
def format_time(timestamp, format='DATE_TIME'):
    if not timestamp:
        return ''
    
    # settings.py에 설정된 시간대(Asia/Seoul)로 시간을 올바르게 변환합니다.
    local_time = timezone.localtime(timestamp)
    
    # Django의 표준 로컬라이제이션 기능(formats.py)을 사용하는 dateformat.format 함수로 변경합니다.
    text = dateformat.format(local_time, formats.get_format(format, use_l10n=True))
    
    return mark_safe('<time datetime="%s" data-format="%s">%s</time>'
        % (timestamp.isoformat(), formats.get_format(format, use_l10n=True), text))

# @register.simple_tag
# def format_time(timestamp, format='DATE_TIME'):
#     if not timestamp:
#         return ''
#     timestamp2 = timestamp.astimezone(timezone.get_default_timezone())
#     text = formats.date_format(timestamp2, format=format)
#     return mark_safe('<time datetime="%s" data-format="%s">%s</time>'
#         % (timestamp.isoformat(), formats.get_format(format), text))

@register.simple_tag
def percentage(a, b):
    return '' if b == 0 else '%s%%' % (100 * a // b)

@register.filter
def hash(obj):
    return hashlib.md5(str(obj).encode('utf8')).hexdigest()

@register.tag
class puzzleblock(template.Node):
    def __init__(self, parser, token):
        args = token.contents.split()
        if len(args) not in (2, 3):
            raise template.TemplateSyntaxError('Usage: {% puzzleblock block-name [variant] %}')
        self.name = args[1]
        self.variant = args[2] if len(args) > 2 else None

    def render_actual(self, context, name):
        return BlockNode(name, NodeList()).render_annotated(context)

    def render_real(self, context):
        html = self.render_actual(context, self.name + '-html')
        if html:
            return html
        md = self.render_actual(context, self.name + '-md')
        if md:
            return markdown.markdown(strip_spaces_between_tags(md), extensions=['extra'])
        return ''

    def render(self, context):
        ident = self.name.replace('-', '_')
        if self.variant:
            context['variant'] = self.variant
            ident += '_' + self.variant
        context[ident] = mark_safe(self.render_real(context))
        return ''

@register.tag
def spacelesser(parser, token):
    nodelist = parser.parse(('endspacelesser',))
    parser.delete_first_token()
    return SpacelesserNode(nodelist)

class SpacelesserNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def replace(self, match):
        if match.start() == 0 or match.string[match.start() - 1] == '>':
            return ''
        if match.end() == len(match.string) or match.string[match.end()] == '<':
            return ''
        return ' '

    def render(self, context):
        return re.sub(r'\s+', self.replace, self.nodelist.render(context))

# <힌트 수정> 아래 코드 전부 추가

class CannedHintNode(template.Node):
    def __init__(self, hint_id, nodelist):
        self.hint_id = hint_id.strip('"\'') # 따옴표 제거
        self.nodelist = nodelist

        # 각 섹션을 파싱하여 저장할 변수
        self.title_nodelist = NodeList()
        self.content_nodelist = NodeList()

        # nodelist에서 hint_title과 hint_content를 찾아서 분리
        for node in nodelist:
            if isinstance(node, CannedHintSectionNode):
                if node.section_name == 'hint_title':
                    self.title_nodelist.extend(node.nodelist)
                elif node.section_name == 'hint_content':
                    self.content_nodelist.extend(node.nodelist)

    def render(self, context):
        # HTML 생성을 분리하고, Python에서는 데이터 준비만 하도록 로직을 대폭 수정했습니다.
        # 'puzzle' 객체를 컨텍스트에서 안전하게 가져오도록 수정
        request = context.get('request')
        if not request:
            return "<!-- CannedHint Error: Request object not found in context. -->"

        # 'Context' 객체에는 .get() 메소드가 없으므로, getattr()을 사용하여 안전하게 속성에 접근합니다.
        custom_context = getattr(request, 'context', None)
        puzzle = getattr(custom_context, 'puzzle', None) if custom_context else None
        team = getattr(custom_context, 'team', None) if custom_context else None
        
        unlocked_ids = context.get('unlocked_canned_hint_ids', set())

        # URL 생성을 위해 puzzle 객체가 필요
        if not puzzle:
            return "<!-- CannedHint Error: Puzzle object not found. -->"
        
        # 템플릿에 전달할 데이터(context)를 준비합니다.
        template_context = {
            'request': request,
            'team': team,
            'puzzle': puzzle,
            'csrf_token': context.get('csrf_token'), # 템플릿에 CSRF 토큰을 전달합니다.
            'hint_id': self.hint_id,
            'title': self.title_nodelist.render(context).strip(),
            'content': self.content_nodelist.render(context).strip(),
            'is_unlocked': self.hint_id in unlocked_ids,
            'action_url': reverse('hints', args=[puzzle.slug]),
        }

        # hint_canned_display.html 템플릿을 사용하여 HTML을 렌더링합니다.
        return render_to_string('hint_canned_display.html', template_context)

class CannedHintSectionNode(template.Node):
    def __init__(self, section_name, nodelist):
        self.section_name = section_name
        self.nodelist = nodelist

    def render(self, context):
        # 이 노드는 직접 렌더링되지 않고, CannedHintNode가 내용을 가져가서 사용합니다.
        return ""

@register.tag(name="canned_hint")
def do_canned_hint(parser, token):
    # 태그 인자 파싱 (e.g., {% canned_hint "my-hint-id" %})
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'canned_hint' tag requires exactly one argument (the hint_id).")
    hint_id_str = bits[1]

    # {% end_canned_hint %} 태그까지의 모든 내용을 파싱합니다.
    nodelist = parser.parse(('end_canned_hint',))
    parser.delete_first_token()

    return CannedHintNode(hint_id_str, nodelist)

# 파서가 '{% hint_title %}' 블록을 하나의 단위로 인식하도록 돕는 헬퍼 태그입니다.
@register.tag(name="hint_title")
def do_hint_title(parser, token):
    nodelist = parser.parse(('end_hint_title',))
    parser.delete_first_token()
    return CannedHintSectionNode('hint_title', nodelist)
    
# 파서가 '{% hint_content %}' 블록을 하나의 단위로 인식하도록 돕는 헬퍼 태그입니다.
@register.tag(name="hint_content")
def do_hint_content(parser, token):
    nodelist = parser.parse(('end_hint_content',))
    parser.delete_first_token()
    return CannedHintSectionNode('hint_content', nodelist)
