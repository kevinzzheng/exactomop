from django import template
register = template.Library()
@register.filter(name='attr')
def attr(obj, name):
    return getattr(obj, name)
