from modules.ply_lex import LexToken
import modules.rd_parcer.sujeto as Sujeto

class Verbo:
    """Representa el grupo verbal: negación opcional, verbo, objeto opcional y adverbios."""
    def __init__(self, negacion: LexToken | None, verbo: LexToken, objeto: Sujeto.Sujetos | None):
        self.negacion = negacion
        self.verbo = verbo
        self.objeto = objeto
        # Lista de tokens ADVERBIO que modifican al verbo
        self.adverbios: list[LexToken] = []
