from modules import ply_lex as _lex
from modules import lexer_rules as _rules
from modules import state

_rules.onCharError = lambda char, line: state.error(line, f"Caracter no permitido '{char}'")
_lexer = _lex.lex(module=_rules)

def tokens(source):
    _lexer.input(source)
    
    while True:
        token = _lex.token()
        if (not token): break
        yield token
    
    eofToken = _lex.LexToken()
    eofToken.type = _rules.Token.EOF
    eofToken.value = None
    eofToken.lineno = _lexer.lineno
    eofToken.lexpos = _lexer.lexpos


    yield eofToken

