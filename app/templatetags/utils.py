import os
from django import template 

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value.name if hasattr(value, 'name') else str(value))