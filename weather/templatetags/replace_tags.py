from django import template
import datetime

register = template.Library()

@register.filter
def replace_space(value):
    return value.replace(" ","")

@register.filter
def upper(value):
    return value.upper()

def fdate(value):
    return format_date(value, "EEEE, d.M.yyyy", locale='el')