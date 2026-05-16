from django import template

register = template.Library()

FLAGS = {

    'Mexico': 'mx',
    'Sudáfrica': 'za',
    'Corea del Sur': 'kr',
    'Rep. Checa': 'cz',
    'Brasil': 'br',
    'Argentina': 'ar',
    'España': 'es',
    'Francia': 'fr',
    'Alemania': 'de',
    'Inglaterra': 'gb',
    'Estados Unidos': 'us',
    'Japón': 'jp',
    'Italia': 'it',
    'Portugal': 'pt',
    'Uruguay': 'uy',
    'Croacia': 'hr',
    'Marruecos': 'ma',
    'Canadá': 'ca',
    'Australia': 'au',
    'Países Bajos': 'nl',

}

@register.filter
def flag_code(country):

    return FLAGS.get(country, 'un')