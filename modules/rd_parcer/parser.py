from modules.lexer_rules import Token
from modules.ply_lex import LexToken
from modules import state
import modules.rd_parcer.sujeto as Sujeto
import modules.rd_parcer.verbo as Verbo
import modules.rd_parcer.complemento as Complemento
import modules.rd_parcer.oraciones as Oraciones


class RDParser:
    def __init__(self, tokens: list[LexToken]):
        self.tokens: list[LexToken] = tokens
        self.current: int = 0

    # ---------------- Utilidades básicas ----------------

    def peek(self) -> LexToken:
        return self.tokens[self.current]

    def previous(self) -> LexToken:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == Token.EOF

    def advance(self) -> LexToken:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type: Token) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, *types: Token) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type: Token, message: str) -> LexToken:
        if self.check(token_type):
            return self.advance()
        raise _error(self.peek(), message)

    # ---------------- Punto de entrada ----------------

    def parse(self):
        """parrafo -> oracion* EOF"""
        oraciones: list[Oraciones.Oracion] = []

        while not self.is_at_end():
            # Si el siguiente token es EOF, terminamos
            if self.check(Token.EOF):
                break
            oraciones.append(self.oracion())

        return oraciones

    # ---------------- Gramática de alto nivel ----------------

    def oracion(self) -> Oraciones.Oracion:
        """oracion -> oracion_svo"""
        return self.oracion_svo()

    def oracion_svo(self) -> Oraciones.OracionSVO:
        """
        oracion_svo -> sujetos verbo adverbios? complemento? .
        """
        sujeto = self.sujetos()
        verbo = self.verbo()

        # adverbios opcionales que modifican al verbo
        adverbios = self.adverbios_opt()
        verbo.adverbios = adverbios

        # complemento preposicional opcional
        complemento = self.complemento_opt()

        # punto final obligatorio
        self.consume(Token.PUNTO, "Se esperaba un '.' al final de la oración.")

        return Oraciones.OracionSVO(sujeto, verbo, complemento)

    # ---------------- Sujetos ----------------

    def sujetos(self) -> Sujeto.Sujetos:
        """sujetos -> sujeto ('Y' sujeto)*"""
        sujetos: list[Sujeto.Sujeto] = []
        sujetos.append(self.sujeto())

        while self.match(Token.Y):
            sujetos.append(self.sujeto())

        return Sujeto.Sujetos(sujetos)

    def sujeto(self) -> Sujeto.Sujeto:
        """sujeto -> sujeto_det | nombre"""
        if self.check(Token.DETERMINANTE) or self.check(Token.SUSTANTIVO):
            return self.sujeto_det()
        if self.check(Token.NOMBRE_PROPIO):
            return self.nombre()

        raise _error(self.peek(), "Se esperaba un sujeto (determinante/sustantivo/nombre propio).")

    def sujeto_det(self) -> Sujeto.SujetoDet:
        """sujeto_det -> 'DETERMINANTE'? 'SUSTANTIVO' 'ADJETIVO'?"""
        determinante = None
        if self.match(Token.DETERMINANTE):
            determinante = self.previous()

        sustantivo = self.consume(Token.SUSTANTIVO, "Se esperaba un sustantivo en el sujeto.")

        adjetivo = None
        if self.match(Token.ADJETIVO):
            adjetivo = self.previous()

        return Sujeto.SujetoDet(determinante, sustantivo, adjetivo)

    def nombre(self) -> Sujeto.Nombre:
        """nombre -> 'NOMBRE_PROPIO' 'ADJETIVO'?"""
        nombre = self.consume(Token.NOMBRE_PROPIO, "Se esperaba un nombre propio.")

        adjetivo = None
        if self.match(Token.ADJETIVO):
            adjetivo = self.previous()

        return Sujeto.Nombre(nombre, adjetivo)

    # ---------------- Verbo y objeto ----------------

    def verbo(self) -> Verbo.Verbo:
        """verbo -> 'NO'? 'VERBO' objeto?"""
        negacion = None
        if self.match(Token.NO):
            negacion = self.previous()

        if not self.match(Token.VERBO):
            raise _error(self.peek(), "Se esperaba un verbo.")

        verbo_token = self.previous()

        objeto = None
        # Un objeto empieza igual que un sujeto (det/sus/nombre propio)
        if self.check(Token.DETERMINANTE) or self.check(Token.SUSTANTIVO) or self.check(Token.NOMBRE_PROPIO):
            objeto = self.sujetos()

        return Verbo.Verbo(negacion, verbo_token, objeto)

    def adverbios_opt(self) -> list[LexToken]:
        """adverbios? -> ('ADVERBIO')*"""
        adverbios: list[LexToken] = []
        while self.match(Token.ADVERBIO):
            adverbios.append(self.previous())
        return adverbios

    # ---------------- Complemento ----------------

    def complemento_opt(self):
        """complemento? -> 'PREPOSICION' sujeto | ε"""
        if self.match(Token.PREPOSICION):
            pre = self.previous()
            sujeto = self.sujeto()
            return Complemento.ComplementoPre(pre, sujeto)
        return None


## Error class to stop parsing
class ParseError(RuntimeError):
    pass


def _error(token: LexToken, message: str) -> ParseError:
    state.parseError(token, message)
    return ParseError()
