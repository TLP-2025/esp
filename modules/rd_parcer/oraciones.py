from ply.lex import LexToken
import modules.rd_parcer.sujeto as Sujeto
import modules.rd_parcer.verbo as Verbo
import modules.rd_parcer.complemento as Complemento

class Oracion: ...

class OracionSVO(Oracion):
    def __init__(self, sujeto: Sujeto.Sujeto, verbo: Verbo.Verbo, complemento: Complemento.Complemento):
        self.sujeto = sujeto
        self.verbo = verbo
        self.complemento = complemento