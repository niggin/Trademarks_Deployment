from django import template
import random

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def random_quote():
    quote = random.randint(0,100)
    return quote