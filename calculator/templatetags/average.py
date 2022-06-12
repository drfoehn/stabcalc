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
def stdv_tot(setting: Setting, duration: Duration):
    return setting.stdv_tot(duration)

@register.simple_tag
def cv(subject: Subject, duration: Duration):
    return subject.cv(duration)

@register.simple_tag
def cv_tot(setting: Setting, duration: Duration):
    return setting.cv_tot(duration)

@register.simple_tag
def avg_tot_sd_h(setting: Setting, duration: Duration):
    return setting.avg_tot_sd_h(duration)

@register.simple_tag
def avg_tot_sd_l(setting: Setting, duration: Duration):
    return setting.avg_tot_sd_l(duration)

@register.simple_tag
def deviation(subject: Subject, duration: Duration):
    return subject.deviation(duration)

@register.simple_tag
def deviation_tot(setting: Setting, duration: Duration):
    return setting.deviation(duration)

# def current_subject(value): # Only one argument.
#     """Converts a string into all lowercase"""
#     return value.self

# TODO: Funktion funzt nicht - Alternativ derzeit .count im templatetag
# @register.simple_tag
# def number_of_subjects(subject: Subject, setting: Setting):
#     return subject.number_of_subjects(setting)
