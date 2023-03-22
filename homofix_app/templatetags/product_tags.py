from django import template
register = template.Library()

@register.simple_tag
def call_sellprice(price,quantity):
    sell_price = price*quantity
    return sell_price