from django import template

register = template.Library()

@register.filter
def eq(value, arg):
    return True if value == arg else False
