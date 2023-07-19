from django import template

register = template.Library()

@register.filter
def get_time_value(time_dict):
    return time_dict.get('value')

@register.filter
def get_time_unit(time_dict):
    return time_dict.get('unit')

@register.filter
def convert_time(value):
    value = float(value)
    minutes = value
    unit = 'minutes'

    if minutes < 60:
        return {"value": minutes, "unit": unit}

    hours = minutes / 60
    unit = 'hours'
    if hours < 24:
        return {"value": hours, "unit": unit}

    days = hours / 24
    unit = 'days'
    if days < 7:
        return {"value": days, "unit": unit}

    weeks = days / 7
    unit = 'weeks'
    if weeks < 4:
        return {"value": weeks, "unit": unit}

    months = weeks / 4
    unit = 'months'
    if months < 12:
        return {"value": months, "unit": unit}

    years = months / 12
    unit = 'years'
    return {"value": years, "unit": unit}
