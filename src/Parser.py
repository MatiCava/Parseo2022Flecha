from sly import Parser
from .lexer import Flecha_Lexer
from .AST import ExprChar, ExprEmpty, ExprNumber, ExprVar, ExprApply

class Flecha_Parser(Parser):
    tokens = lexer.tokens

    precedence = (
       ('left', OR),
       ('left', AND),
       ('right', NOT),
       ('left', EQ, NE, GE, LE, GT, LT),       
       ('left', PLUS, MINUS),
       ('left', TIMES),
       ('left', DIV, MOD),
       ('right', UMINUS),
    )

    @_('')
    def programa(self, p):
        return ExprEmpty()
    
    @_('programa definicion')
    def programa(self, p):
        return

    @_('DEF LOWERID parametros DEFEQ expresion')
    def definicion(self, p):
        return

    @_('LOWERID parametros')
    def parametros(self, p):
        return 

    @_('empty')
    def parametros(self, p):
        return

    @_('expresionExterna')
    def expresion(self, p):
        return

    @_('expresionExterna SEMICOLON expresion')
    def expresion(self, p):
        return

    @_('expresionIf', 'expresionCase', 'expresionLet', 'expresionLambda', 'expresionInterna')
    def expresionExterna(self, p):
        return

    @_('IF expresionInterna THEN expresionInterna ramasElse')
    def expresionIf(self, p):
        return

    @_('ELIF expresionInterna THEN expresionInterna ramasElse')
    def ramasElse(self, p):
        return

    @_('ELSE expresionInterna')
    def ramasElse(self, p):
        return

    @_('CASE expresionInterna ramasCase')
    def expresionCase(self, p):
        return

    @_('empty')
    def ramasCase(self, p):
        return

    @_('ramaCase ramasCase')
    def ramasCase(self, p):
        return

    @_('PIPE UPPERID parametros ARROW expresionInterna')
    def ramaCase(self, p):
        return

    @_('LET LOWERID parametros DEFEQ expresionInterna IN expresionExterna')
    def expresionLet(self, p):
        return

    @_('LAMBDA parametros ARROW expresionExterna')
    def expresionLambda(self, p):
        return

    @_('expresionAplicacion')
    def expresionInterna(self, p):
        return

    @_('expresionInterna AND expresionInterna')
    @_('expresionInterna OR expresionInterna')
    @_('expresionInterna EQ expresionInterna')
    @_('expresionInterna NE expresionInterna')
    @_('expresionInterna GE expresionInterna')
    @_('expresionInterna LE expresionInterna')
    @_('expresionInterna GT expresionInterna')
    @_('expresionInterna LT expresionInterna')
    @_('expresionInterna PLUS expresionInterna')
    @_('expresionInterna MINUS expresionInterna')
    @_('expresionInterna TIMES expresionInterna')
    @_('expresionInterna DIV expresionInterna')
    @_('expresionInterna MOD expresionInterna')
    def expresionInterna(self, p):
        return ExprApply(ExprApply(ExprVar(p[1]), p[0]),  p[2])

    @_('NOT expresionInterna')
    @_('UMINUS expresionInterna')
    def expresionInterna(self, p):
        return

    @_('expresionAtomica')
    def expresionAplicacion(self, p):
        return

    @_('expresionAplicacion expresionAtomica')
    def expresionAplicacion(self, p):
        return ExprApply(p[0], p[1])

    @_('LOWERID')
    def expresionAtomica(self, p):
        return ExprVar(p[0])

    @_('UPPERID')
    def expresionAtomica(self, p):
        return

    @_('NUMBER')
    def expresionAtomica(self, p):
        return ExprNumber(p[0])

    @_('CHAR')
    def expresionAtomica(self, p):
        return ExprChar(p[0])

    @_('STRING')
    def expresionAtomica(self, p):
        return

    @_('LPAREN expresion RPAREN')
    def expresionAtomica(self, p):
        return
