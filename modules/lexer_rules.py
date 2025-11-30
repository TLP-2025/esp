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
    PUNTO = 'PUNTO'


    #END
    EOF = 'EOF'

# Mapping for lex library
tokens = tuple(map(lambda name: Token[name].value, Token._member_names_,))


# Regular expression rules
## Single-character tokens.
t_DETERMINANTE = r'det:\w+'
t_SUSTANTIVO = r'sus:\w+'
t_ADJETIVO = r'adj:\w+'
t_NOMBRE_PROPIO = r'nom:\w+'
t_PREPOSICION = r'pre:\w+'
t_VERBO = r'ver:\w+'

t_NO = r'no'
t_Y = r'y'
t_PUNTO = r'\.'



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' ,:;?!\t'  

def onCharError(char, line): ...

# Error handling rule
def t_error(t):
    onCharError(t.value[0], t.lexer.lineno)
    t.lexer.skip(1)
