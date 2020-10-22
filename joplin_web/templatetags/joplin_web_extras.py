from django.conf import settings
from django import template
import arrow

register = template.Library()


@register.filter(name='date_to_timestamp')
def date_to_timestamp(value):
    utc = arrow.get(value)
    local = utc.to(settings.USE_TZ)
    return local

