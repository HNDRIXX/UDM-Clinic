# app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def split_name(value):
    names = value.split(" ")
    return names[0]
