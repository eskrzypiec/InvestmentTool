from django import template

register = template.Library()


@register.filter(name='format_date')
def format_date(date):
    return date.strftime("%Y-%m-%d")


