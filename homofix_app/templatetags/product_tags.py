from django import template
from decimal import Decimal
register = template.Library()

@register.simple_tag
def call_sellprice(price,quantity):
    sell_price = price*quantity
    return sell_price

@register.simple_tag
def call_gst(subtotal):
    total_amt = (call_sellprice*18)/100
    return total_amt


@register.simple_tag
def call_sellprice(price, quantity):
    return Decimal(price) * Decimal(quantity)