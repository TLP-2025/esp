from modules.ply_lex import LexToken
import modules.rd_parcer.sujeto as Sujeto

class Complemento:
    ...
    
class ComplementoPre(Complemento):
    def __init__(self, preposicion: LexToken, sujeto: Sujeto.Sujeto):
        self.preposicion = preposicion
        self.sujeto = sujeto