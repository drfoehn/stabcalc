from django import template
from calculator.models import *

register = template.Library()


@register.simple_tag
def average(subject: Subject, duration: Duration):
    return subject.average(duration)

@register.simple_tag
def average_tot(setting: Setting, duration: Duration):
    return setting.average_tot(duration)

@register.simple_tag
def stdv(subject: Subject, duration: Duration):
    return subject.stdv(duration)

@register.simple_tag
def cv(subject: Subject, duration: Duration):
    return subject.cv(duration)

# TODO: Funktion funzt nicht - Alternativ derzeit .count im templatetag
# @register.simple_tag
# def number_of_subjects(subject: Subject, setting: Setting):
#     return subject.number_of_subjects(setting)
