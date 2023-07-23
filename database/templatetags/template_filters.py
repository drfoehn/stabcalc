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


@register.filter
def is_not_empty_m2m_field_or(m2m_field, field_names_string):
    """
    Checks if a specific field in a M2M field is empty or not.

    Args:
      m2m_field: The M2M field to check.
      field_names_string: A string of field names separated by a comma.

    Returns:
      True if the field is not empty, False otherwise.
    """

    # Split the field names string into a list of field names.
    field_names = field_names_string.split(',')

    if m2m_field.filter(**{f"{field_name}__isnull": False for field_name in field_names}).exists():
        return True
    else:
        return False

@register.filter(name='dict_key')
def dict_key(dict, key):
    '''Returns the given key from a dictionary.'''
    return dict[key]