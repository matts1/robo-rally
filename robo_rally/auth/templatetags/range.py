from django.template import Library

register = Library()


# filter to do range in django template
@register.filter(name='range')
def get_range(value):
    return range(value)
