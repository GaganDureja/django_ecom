
from django import template

register = template.Library()


@register.simple_tag
def percent_discount(price, mrp):
    try:
        # return addtional_dis
        return "-%d%%" % round(100 - (price / mrp * 100))
    except (ValueError, ZeroDivisionError):
        return ""
    
# @register.filter
# def as_percentage_of(part, whole):
#     try:
#         return "%d%%" % (float(part) / whole * 100)
#     except (ValueError, ZeroDivisionError):
#         return ""