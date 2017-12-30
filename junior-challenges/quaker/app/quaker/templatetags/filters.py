import re
from django import template

register = template.Library()

@register.filter
def xss_filter(s):
    return re.sub('(script|on[^=]+=)', '####', s, flags=re.IGNORECASE)
