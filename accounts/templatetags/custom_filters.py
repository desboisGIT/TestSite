from django import template

register = template.Library()

@register.filter
def uppercase_and_slice(value):
    if isinstance(value, str):
        return value.upper()[:9]
    return value