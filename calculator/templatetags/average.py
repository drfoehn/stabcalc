from django import template
from calculator.models import *

register = template.Library()


@register.simple_tag
def average(subject: Subject, duration: Duration):
    return subject.average(duration)

@register.simple_tag
def stdv(subject: Subject, duration: Duration):
    return subject.stdv(duration)

@register.simple_tag
def cv(subject: Subject, duration: Duration):
    return subject.cv(duration)