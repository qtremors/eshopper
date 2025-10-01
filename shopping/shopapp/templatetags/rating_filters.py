# templatetags/rating_filters.py

from django import template
register = template.Library()

@register.filter
def floatdiv(value, arg):
    return int(float(value) // float(arg))

@register.filter
def floatmod(value, arg):
    return float(value) % float(arg)
