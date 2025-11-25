from ply.lex import LexToken
import modules.rd_parcer.sujeto as Sujeto

class Verbo:
    def __init__(self, negacion: LexToken, verbo: LexToken, objeto: Sujeto.Sujetos):
        self.negacion = negacion
        self.verbo = verbo
        self.objeto = objeto