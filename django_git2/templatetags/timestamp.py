from django.conf import settings
from django import template
from django.template.defaulttags import TemplateIfParser, IfNode

import time
import datetime


register = template.Library()

@register.filter(expects_localtime=True, is_safe=False)
def timestamp(value, arg=None):
    """Formats a timestamp according to the given format."""

    if value in (None, u''):
        return u''
    if arg is None:
        arg = settings.TIME_FORMAT
    t = time.gmtime(int(value))
    return time.strftime(arg, t)

@register.filter(expects_localtime=True, is_safe=False)
def timestamp2date(value, arg=None):
    """Formats a timestamp according to the given format."""

    if value in (None, u''):
        return u''
    t = time.gmtime(int(value))
    d = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return d

@register.filter(expects_localtime=True, is_safe=False)
def duration(value, arg=None):
    """calc a minites about timestamp until now."""

    if value in (None, u''):
        return 0
    s = int(value)
    now = time.time()
    return int((now - s)/60)
