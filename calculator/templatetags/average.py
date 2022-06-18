from django import template
from calculator.models import *
import math

register = template.Library()


@register.simple_tag
def average(subject: Subject, duration: Duration):
    if subject.average(duration) is None:
        return ""
    return subject.average(duration)

@register.simple_tag
def average_tot(setting: Setting, duration: Duration):
    if setting.average_tot(duration) is None:
        return ""
    return setting.average_tot(duration)

@register.simple_tag
def stdv(subject: Subject, duration: Duration):
    if subject.stdv(duration) is None:
        return ""
    return subject.stdv(duration)

@register.simple_tag
def stdv_tot(setting: Setting, duration: Duration):
    if setting.stdv_tot(duration) is None:
        return ""
    return setting.stdv_tot(duration)

@register.simple_tag
def cv(subject: Subject, duration: Duration):
    if subject.cv(duration) is None:
        return ""
    return subject.cv(duration)

@register.simple_tag
def cv_tot(setting: Setting, duration: Duration):
    if setting.cv_tot(duration) is None:
        return ""
    return setting.cv_tot(duration)

@register.simple_tag
def avg_tot_sd_h(setting: Setting, duration: Duration):
    if setting.avg_tot_sd_h(duration) is None:
        return ""
    return setting.avg_tot_sd_h(duration)

@register.simple_tag
def avg_tot_sd_l(setting: Setting, duration: Duration):
    if setting.avg_tot_sd_l(duration) is None:
        return ""
    return setting.avg_tot_sd_l(duration)

@register.simple_tag
def deviation(subject: Subject, duration: Duration):
    if subject.deviation(duration) is None:
        return ""
    return subject.deviation(duration)


@register.simple_tag
def deviation_tot(setting: Setting, duration: Duration):
    if setting.deviation_tot(duration) is None:
        return ""
    return setting.deviation_tot(duration)

# @register.simple_tag #FIXME: Does not work
# def seconds_to_text(setting: Setting, duration:Duration):
#     return setting.seconds_to_text(duration)

# def current_subject(value): # Only one argument.
#     """Converts a string into all lowercase"""
#     return value.self

# TODO: Funktion funzt nicht - Alternativ derzeit .count im templatetag
# @register.simple_tag
# def number_of_subjects(subject: Subject, setting: Setting):
#     return subject.number_of_subjects(setting)


@register.filter(name="human_readable_seconds")
def human_readable_seconds(secs: int):
    years = secs // (86400 * 365)  # TODO: muss ich noch neu berechnen
    months = secs // (86400 * 30)   # TODO: muss ich noch neu berechnen
    weeks = secs // (86400*7)
    days = secs // 86400
    hours = (secs - days * 86400) // 3600
    minutes = (secs - days * 86400 - hours * 3600) // 60
    seconds = secs - days * 86400 - hours * 3600 - minutes * 60
    result = ("{0} year{1} ".format(years, "s" if years != 1 else "") if years else "") + \
             ("{0} month{1} ".format(months, "s" if months != 1 else "") if months else "") + \
             ("{0} week{1} ".format(weeks, "s" if weeks != 1 else "") if weeks else "") + \
             ("{0} day{1} ".format(days, "s" if days != 1 else "") if days else "") + \
             ("{0} hour{1} ".format(hours, "s" if hours != 1 else "") if hours else "") + \
             ("{0} minute{1} ".format(minutes, "s" if minutes != 1 else "") if minutes else "Baseline") + \
             ("{0} second{1} ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
    return result
