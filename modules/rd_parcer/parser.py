from modules.lexer_rules import Token
from ply.lex import LexToken
from modules import state
import modules.rd_parcer.sujeto as Sujeto
import modules.rd_parcer.verbo as Verbo
import modules.rd_parcer.complemento as Complemento
import modules.rd_parcer.oraciones as Oraciones



class RDParser:
    def __init__(self,tokens:list[LexToken]):
        self.tokens: list[LexToken] = tokens
        self.current: int = 0

    
    def parse(self) -> list[Oraciones.Oracion]:
        parrafo: list[Oraciones.Oracion] = []

        while (not self.isAtEnd()):
            parrafo.append(self.oracion())

        return parrafo

    # RD methods

    def oracion(self) -> Oraciones.Oracion:
        try:
            return self.oracionSVO()
        except ParseError as e:
            self._synchronize()
            return None
    


    def oracionSVO(self) -> Oraciones.OracionSVO:
        sujeto: Sujeto.Sujetos = self.sujetos()
        verbo:Verbo.Verbo = self.verbo()

        complemento:Complemento.Complemento = None
        if (self.match(Token.PREPOSICION)):
            complemento = self.complemento_pre()
        
        self.consume(Token.PUNTO, "Se esperaba un punto al final de la oración")

        return Oraciones.OracionSVO(sujeto, verbo, complemento)
    

    
    def sujetos(self) -> Sujeto.Sujetos:
        
        sujetos: list[Sujeto.Sujeto] = []
        sujetos.append(self.sujeto())

        while (self.match(Token.Y)):
            sujetos.append(self.sujeto())
        
        return Sujeto.Sujetos(sujetos)

    
    def sujeto(self) -> Sujeto.Sujeto:
        if (self.match(Token.NOMBRE_PROPIO)):
            return self.nombre()
        
        return self.sujeto_det()

    def nombre(self) -> Sujeto.Nombre:
        nombre: LexToken = self.previous()
        adjetivo: LexToken = None
        if (self.match(Token.ADJETIVO)):
            adjetivo = self.previous()
        
        return Sujeto.Nombre(nombre, adjetivo)
    
    def sujeto_det(self) -> Sujeto.SujetoDet:
        determinante: LexToken = None
        adjetivo: LexToken = None

        if (self.match(Token.DETERMINANTE)):
            determinante = self.previous()
        
        sustantivo: LexToken = self.consume(Token.SUSTANTIVO, "Se esperaba un sustantivo")

        if (self.match(Token.ADJETIVO)):
            adjetivo = self.previous()

        return Sujeto.SujetoDet(determinante, sustantivo, adjetivo)



    
    def verbo(self) -> Verbo.Verbo:
        negacion: LexToken = None
        if (self.match(Token.NO)):
            negacion = self.previous()
        
        if (not self.match(Token.VERBO_SINGULAR,Token.VERBO_PLURAL)):
            raise _error(self.peek(), "Se esperaba un verbo")
        
        verb: LexToken = self.previous()

        
        # objeto opcional
        objeto: Sujeto.Sujetos = None
        match self.peek().type:
            case Token.DETERMINANTE | Token.NOMBRE_PROPIO | Token.SUSTANTIVO:
                objeto = self.sujetos()
        
        return Verbo.Verbo(negacion, verb, objeto)

        

    
    def complemento_pre(self) -> Complemento.ComplementoPre:
        preposicion:LexToken = self.previous()

        sujeto = self.sujeto()

        return Complemento.ComplementoPre(preposicion, sujeto)





    # Base methods
        
        
    def consume(self, type: Token, msg:str):
        if (self.check(type)): return self.advance()

        raise _error(self.peek(), msg)

    def match(self, *tokenTypes: Token) -> bool:
        for t in tokenTypes:
            if (self.check(t)):
                self.advance()
                return True
            
        return False
    

    def check(self, tokenType: Token) -> bool: 
        if (self.isAtEnd()): return False
        return self.peek().type == tokenType.value
    
    def advance(self) -> LexToken:
        if (not self.isAtEnd()): self.current+=1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().type == Token.EOF
    
    def peek(self) -> LexToken:
        return self.tokens[self.current]

    def previous(self) -> LexToken:
        return self.tokens[self.current-1]
    
    
    ## Error handling
    # Ignorar tokens hasta '.' o inicio de oracion (sujeto)
    def _synchronize(self):
        self.advance()

        while(not self.isAtEnd()):
            if (self.previous().type == Token.PUNTO): return

            match self.peek().type:
                case Token.DETERMINANTE| Token.SUSTANTIVO | Token.NOMBRE_PROPIO:
                    return
                
            self.advance()

                
## Error class to stop parsing
class ParseError(RuntimeError): ...

def _error(token: LexToken, message: str) -> ParseError:
    state.parseError(token, message)
    return ParseError()
