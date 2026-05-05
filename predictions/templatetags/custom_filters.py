from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def porcentaje(valor, maximo):
    try:
        if maximo == 0 or maximo is None:
            return 0
        return (valor / maximo) * 100
    except:
        return 0