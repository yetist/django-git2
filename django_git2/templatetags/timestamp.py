from django.template.base import Node, NodeList, TemplateSyntaxError, VariableDoesNotExist
from django.conf import settings
from django import template

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

@register.filter(expects_localtime=True, is_safe=False)
def getline(value, arg=None):
    """calc a minites about timestamp until now."""

    if value in (None, u''):
        return u''
    lines = value.splitlines()
    if arg is None:
        arg = "0"
    try:
        msg = eval("lines["+arg+"]")
    except IndexError:
        msg = u''
    if type(msg) == type([]):
        msg = "\n".join(msg)
    return msg

class RefsNode(Node):
    def __init__(self, commit, refs, nodelist_true, nodelist_false):
        self.commit = commit
        self.refs = refs
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfDecoNode>"

    def render(self, context):
        try:
            commit = self.commit.resolve(context, True)
        except VariableDoesNotExist:
            commit = []
        try:
            refs = self.refs.resolve(context, True)
        except VariableDoesNotExist:
            refs = []

        ref = context['ref'] = {
                'type':u'',
                'name':u'',
                }
        for k, v in refs['branches']:
            if commit.hex == v.hex:
                ref['type'] = u"branch"
                ref['name'] = k
        for k, v in refs['tags']:
            if commit.hex == v.hex:
                ref['type'] = u"tag"
                ref['name'] = k
        if ref['type'] != u'':
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

@register.tag('ifref')
def do_ifref(parser, token):
    """
    Outputs the contents of the block if the commit is a branch or tag.
    Test commit is a git reference, 

    {% ifref commit in refs %}{{ ref.type }} {{ ref.name }} {% endifref %}

    if commit in refs, ref.type will be "branch" or "tag"; ref.name will be the name of the ref.
    """

    bits = token.split_contents()
    if len(bits) < 4:
        raise TemplateSyntaxError("'showdeco' statements should have at least four"
                                  " words: %s" % token.contents)
    if bits[-2] != 'in':
        raise TemplateSyntaxError("'showdeco' statements should use the format"
                                  " 'showdeco commit in references': %s" % token.contents)
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    commit = parser.compile_filter(bits[1])
    refs = parser.compile_filter(bits[3])
    return RefsNode(commit, refs, nodelist_true, nodelist_false)
