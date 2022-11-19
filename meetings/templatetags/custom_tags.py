from django import template

register = template.Library()


@register.filter
def get_at_index(object_list, index):
    return object_list[index]
