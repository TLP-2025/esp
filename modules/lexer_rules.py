from enum import Enum

class Token(str, Enum):
    DETERMINANTE = 'DETERMINANTE'
    SUSTANTIVO = 'SUSTANTIVO'
    ADJETIVO = 'ADJETIVO'
    NOMBRE_PROPIO = 'NOMBRE_PROPIO'
    PREPOSICION = 'PREPOSICION'
    VERBO = 'VERBO'
    ADVERBIO = 'ADVERBIO'
    NO = 'NO'
    Y = 'Y'
    PUNTO = 'PUNTO'


    #END
    EOF = 'EOF'

# Mapping for lex library
tokens = tuple(map(lambda name: Token[name].value, Token._member_names_,))


def t_DETERMINANTE(t):
    r'det:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_SUSTANTIVO(t):
    r'sus:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_ADJETIVO(t):
    r'adj:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_NOMBRE_PROPIO(t):
    r'nom:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_PREPOSICION(t):
    r'pre:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_VERBO(t):
    r'ver:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    
def t_ADVERBIO(t):
    r'adv:\w+'
    t.value = t.value[t.value.index(':')+1:]
    return t
    

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
