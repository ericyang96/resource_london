from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import math

register = template.Library()

# Round all currency values to the nearest hundred
def currency(pounds):
    pounds = round(pounds / 100.0) * 100
    if pounds >= 0:
        return "£%s" % (intcomma(int(pounds)))
    else:
        return "-£%s" % (intcomma(abs(pounds)))

# Round all non-integer values to 1 decimal place
def decimal(value):
    value = round(float(value) * 100, 1)
    return "%s%%" % value

def no_decimal(value):
    no_decimal_value = int(round(value))
    if no_decimal_value >= 0:
        return "£%s" % no_decimal_value
    else:
        return "-£%s" % abs(no_decimal_value)

register.filter('currency', currency)
register.filter('decimal', decimal)
register.filter('no_decimal', no_decimal)
