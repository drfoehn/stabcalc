from django import template
from calculator.models import Duration, Subject

register = template.Library()


@register.simple_tag
def average(subject: Subject, duration: Duration):
    return subject.average(duration)