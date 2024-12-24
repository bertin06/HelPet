from django import template
from emoji import emojize

register = template.Library()

@register.filter
def convert(request, message):
    return emojize(message)