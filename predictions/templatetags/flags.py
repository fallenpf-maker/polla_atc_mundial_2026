from django import template

register = template.Library()

FLAGS = {

    # ANFITRIONES
    'Estados Unidos': 'us',
    'Mexico': 'mx',
    'Canada': 'ca',
    'Canadá': 'ca',

    # CONMEBOL
    'Argentina': 'ar',
    'Brasil': 'br',
    'Uruguay': 'uy',
    'Colombia': 'co',
    'Ecuador': 'ec',
    'Perú': 'pe',
    'Chile': 'cl',
    'Paraguay': 'py',
    'Bolivia': 'bo',
    'Venezuela': 've',

    # UEFA
    'España': 'es',
    'Francia': 'fr',
    'Alemania': 'de',
    'Inglaterra': 'gb',
    'Italia': 'it',
    'Portugal': 'pt',
    'Países Bajos': 'nl',
    'Holanda': 'nl',
    'Croacia': 'hr',
    'Bélgica': 'be',
    'Suiza': 'ch',
    'Dinamarca': 'dk',
    'Suecia': 'se',
    'Noruega': 'no',
    'Polonia': 'pl',
    'Serbia': 'rs',
    'Austria': 'at',
    'Ucrania': 'ua',
    'Turquía': 'tr',
    'República Checa': 'cz',
    'Rep. Checa': 'cz',
    'Escocia': 'gb',
    'Gales': 'gb',
    'Hungría': 'hu',
    'Grecia': 'gr',
    'Rumania': 'ro',
    'Bosnia y Herc.':'ba',
    'Jordania':'jo',
    # AFC
    'Japón': 'jp',
    'Corea del Sur': 'kr',
    'Corea': 'kr',
    'Australia': 'au',
    'Arabia Saudita': 'sa',
    'Irán': 'ir',
    'Qatar': 'qa',
    'Irak': 'iq',
    'Emiratos Árabes Unidos': 'ae',
    'China': 'cn',
    'Uzbekistán': 'uz',
    'Cabo Verde':'cv',
    'RD Congo':'cd',

    # CAF
    'Marruecos': 'ma',
    'Senegal': 'sn',
    'Egipto': 'eg',
    'Nigeria': 'ng',
    'Camerún': 'cm',
    'Ghana': 'gh',
    'Costa de Marfil': 'ci',
    'Túnez': 'tn',
    'Argelia': 'dz',
    'Sudáfrica': 'za',

    # CONCACAF
    'Costa Rica': 'cr',
    'Panamá': 'pa',
    'Jamaica': 'jm',
    'Honduras': 'hn',
    'El Salvador': 'sv',
    'Haití':'ht',
    'Curazao':'cw',

    # OFC
    'Nueva Zelanda': 'nz',

}

@register.filter
def flag_code(country):

    return FLAGS.get(country, 'un')