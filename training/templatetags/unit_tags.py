from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# tags to help convert from km to mi and back and make templates more manageable

@register.filter
def as_distance(value):
    html = (f'<span class="distance" data-mi="{value}">{value}</span>'
            f'<span class="distance-label"> mi</span>');
    return mark_safe(html)

@register.simple_tag
def pace_display(seconds, mileage, pace_str):
    html = (f'<span class="pace"'
            f'data-seconds="{seconds}"'
            f'data-mi="{mileage}"'
            f'data-mi-pace="{pace_str}">'
            f'{pace_str}</span>'
            f'/<span class="distance-label">mi</span>');
    return mark_safe(html)