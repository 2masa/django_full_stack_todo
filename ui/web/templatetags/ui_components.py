from django import template

register = template.Library()

@register.inclusion_tag('select_option.html')
def drop_down(options, name, id, default_value=""):
    return {
        'options': options,
        'name': name,
        'id': id,
        'default_value': default_value
    }

@register.inclusion_tag('edit_todo.html')
def edit_todo_modal(item, priority_options, status_options):
    return {
        'item': item,
        'priority_options': priority_options,
        'status_options': status_options
    }