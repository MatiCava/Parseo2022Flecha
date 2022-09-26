class Programa:
    def __init__(self,programa,definicion):
        self.pragrama = programa
        self.definicion = definicion
        
    def toAST(self):
        return self.pragrama.toAST() + [self.definicion.toAST()]
        
class ExprDefinicion:
    def __init__(self, id, parametros, expresion):
        self.id = id
        self.listParams = DefParams(parametros,expresion)
    def toAST(self):
        return ["Def", self.id] + [self.node.toAST()]

class DefParams:
    def __init__(self, id=None, values=None):
        self.id = id
        self.values = values
    def toAST(self):
        res = []
        if self.id:
            res.append(self.id)
        res += self.values.toAST()
        return res

class ExprConstructor:
    def __init__(self, id):
        self.id = id
    def toAST(self):
        return ["ExprConstructor", self.id]

class ExprIfThen:
    def __init__(self, condicion, ramaThen, ramaElse):
        self.condicion = condicion
        self.ramaThen = ramaThen
        self.ramaElse = ramaElse
    def toAST(self):
        ramaThen = ["CaseBranch", "True", [], self.ramaThen.toAST()]
        ramaElse = ["CaseBranch", "False", [], self.ramaElse.toAST()]
        return ['ExprCase', self.condicion.toAST(), [ramaThen, ramaElse]]

class ExprCase:
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def toAST(self):
        return ['ExprCase', self.expr1.toAST(), self.expr2.toAST()]

class ExprLet:
    def __init__(self, id, parametros, exp1, exp2):
        self.id = id
        self.parametros = LetParams(parametros, exp1)
        self.exp2 = exp2

    def toAST(self):
        return ["ExprLet", self.id] + [self.node.toAST()] + [self.exp2.toAST()]

class LetParams:
    def __init__(self, values, exp):
        self.values = values
        self.exp = exp
    def toAST(self):
        # expresarse como muchas lambdas anidadas. Por ejemplo, son equivalentes:
        # \ x y z -> x + y
        # \ x -> (\ y -> (\ z -> x + y))
        return;

class ExprChar:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        return ["ExprChar"] + [ord(self.value)] 

class ExprVar:
    def __init__(self, id):
        self.id = id
    def toAST(self):
        return ["ExprVar", self.id]

class ExprNumber:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        return ["ExprNumber", int(self.value)]

class ExprString:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        #Debemos parsear el string como:
        # "hola" -> Cons 'h' (Cons 'o' (Cons 'l' (Cons 'a' Nil)))
        return

class ExprApply:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def toAST(self):
        return ['ExprApply', self.exp1.toAST(), self.exp2.toAST()]

class ExprEmpty:
    def __init__(self):
        self.expr = []
    
    def toAST(self):
        return self.expr
    
