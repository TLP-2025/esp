from ply.lex import LexToken

class Sujeto(): ...

class SujetoDet(Sujeto):
    def __init__(self, determinante: LexToken, sustantivo: LexToken, adjetivo: LexToken):
        self.determinante = determinante
        self.sustantivo = sustantivo
        self.adjetivo = adjetivo

class Nombre(Sujeto):
    def __init__(self, nombre:LexToken, adjetivo: LexToken):
        self.nombre = nombre
        self.adjetivo = adjetivo

class Sujetos():
    def __init__(self, sujetos: list[Sujeto]):
        self.sujetos = sujetos