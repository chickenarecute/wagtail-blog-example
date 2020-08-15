from django import template
from django.template.defaultfilters import stringfilter
from django.template import engines
from django.template.loader import get_template

register = template.Library()

@register.filter(name='upper')
def upper(value):
    print("-> ", dir(value))
    print(">>>> ", value.all())
    print("img url : ", value.model.__dict__)
    return #value.upper()

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<strong>%s</strong>%s' % (esc(first), esc(other))
    return mark_safe(result)


@register.filter(name="render_date")
def render_date(d):


    return str(d)
