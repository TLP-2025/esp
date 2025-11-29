from enum import Enum

class Token(str, Enum):
    DETERMINANTE = 'DETERMINANTE'
    SUSTANTIVO = 'SUSTANTIVO'
    ADJETIVO = 'ADJETIVO'
    NOMBRE_PROPIO = 'NOMBRE_PROPIO'
    PREPOSICION = 'PREPOSICION'
    VERBO = 'VERBO'
    NO = 'NO'
    Y = 'Y'
    ADVERBIO = 'ADVERBIO'
    PUNTO = 'PUNTO'
    EOF = 'EOF'


# Lista de nombres de tokens que usa PLY
tokens = tuple(t.value for t in Token)


# Reglas de expresiones regulares para los tokens
t_DETERMINANTE = r'det:\w+'
t_SUSTANTIVO = r'sus:\w+'
t_ADJETIVO = r'adj:\w+'
t_NOMBRE_PROPIO = r'nom:\w+'
t_PREPOSICION = r'pre:\w+'
t_VERBO = r'vrs:\w+'
t_ADVERBIO = r'adv:\w+'

t_NO = r'no'
t_Y = r'y'
t_PUNTO = r'\.'


# Regla para contar líneas nuevas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Caracteres ignorados (espacios, comas, tabulaciones, etc.)
t_ignore  = ' ,:;?!\t'  


def onCharError(char, line): ...


# Manejo de errores léxicos
def t_error(t):
    onCharError(t.value[0], t.lexer.lineno)
    t.lexer.skip(1)
