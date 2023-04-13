from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def moneda(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

def porcentaje(dollars):
    dollars = round(float(dollars), 2)
    return "%s%s%%" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


register.filter('moneda', moneda)
register.filter('porcentaje', porcentaje)