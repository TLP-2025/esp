from modules.ply_lex import LexToken
import modules.rd_parcer.sujeto as Sujeto

class Verbo:
    def __init__(self, negacion: LexToken, verbo: LexToken, objeto: Sujeto.Sujetos, adverbio: LexToken):
        self.negacion = negacion
        self.verbo = verbo
        self.objeto = objeto
        self.adverbio = adverbio