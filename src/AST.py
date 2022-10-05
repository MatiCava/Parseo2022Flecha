######################## Programa ###################### 
class Programa:
    def __init__(self,programa,definicion):
        self.pragrama = programa
        self.definicion = definicion
        
    def toAST(self):
        return self.pragrama.toAST() + [self.definicion.toAST()]

######################## Definition ######################        
class Definition:
    def __init__(self, id, parametros, expresion):
        self.id = id
        self.node = LetParams(parametros,expresion)
    def toAST(self):
        return ["Def", self.id] + [self.node.toAST()]

######################## ExprVar #######################
class ExprVar:
    def __init__(self, id):
        self.id = id
    def toAST(self):
        return ["ExprVar", self.id]

######################## ExprConstructor ######################
class ExprConstructor:
    def __init__(self, id):
        self.id = id
    def toAST(self):
        return ["ExprConstructor", self.id]

######################## ExprNumber #######################
class ExprNumber:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        return ["ExprNumber", int(self.value)]

######################## ExprChar #######################
class ExprChar:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        return ["ExprChar"] + parseListString(self.value)

######################## ExprCase ######################
class ExprCase:
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def toAST(self):
        return ['ExprCase', self.expr1.toAST(), self.expr2.toAST()]

class ExprCases:
    def __init__(self, caseBranch= None, caseBranches= None):
        self.caseBranch = caseBranch
        self.caseBranches = caseBranches
    def toAST(self):
        res = []
        if self.caseBranch:
            res = [self.caseBranch.toAST()]
        if self.caseBranches:
            res += self.caseBranches.toAST()
        return res

class ExprCaseBranch:
    def __init__(self, id, params, expr):
        self.id = id
        self.params = Params(params)
        self.expr = expr

    def toAST(self):
        return ["CaseBranch", self.id] + [self.params.toAST()] + [self.exp.toAST()]

######################## ExprSemicolon ######################
class ExprSemicolon:
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def toAST(self):
        return ['ExprLet', '_', self.expr1.toAST(), self.expr2.toAST()]

######################## ExprLet ######################
class ExprLet:
    def __init__(self, id, parametros, exp1, exp2):
        self.id = id
        self.node = LetParams(parametros, exp1)
        self.exp2 = exp2

    def toAST(self):
        return ["ExprLet", self.id] + [self.node.toAST()] + [self.exp2.toAST()]

class LetParams:
    def __init__(self, parametros, expresion):
        self.parametros = parametros
        self.expresion = expresion
    def toAST(self):
        tail = self.expresion.toAST()
        for parametro in reversed(self.parametros.toAST()):
            tail = ["ExprLambda", parametro, tail]
        return tail

######################## ExprLambda ######################
class ExprLambda:
    def __init__(self, parametros, expresion):
        self.node = LetParams(parametros, expresion)
    def toAST(self):
        return self.node.toAST()

######################## ExprApply #######################
class ExprApply:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def toAST(self):
        return ['ExprApply', self.exp1.toAST(), self.exp2.toAST()]


######################## OTRAS Expr ######################
class Expr:
    def __init__(self, expr):
        self.expr = expr
    def toAST(self):
        return self.expr.toAST()
class ExprEmpty:
    def toAST(self):
        return []

class Params:
    def __init__(self, id=None, values=None):
        self.id = id
        self.values = values
    def toAST(self):
        res = []
        if self.id:
            res.append(self.id)
        res += self.values.toAST()
        return res
class ExprString:
    def __init__(self, value):
        self.value = value
    def toAST(self):
        tail = ['ExprConstructor', 'Nil'] 
        for ch in reversed(parseListString(self.value)):
            cons = ['ExprConstructor', 'Cons']
            char = ['ExprChar', ch]
            head = ['ExprApply', cons, char]
            tail = ['ExprApply', head, tail]
        return tail
        
class ExprIfThen:
    def __init__(self, condicion, ramaThen, ramaElse):
        self.condicion = condicion
        self.ramaThen = ramaThen
        self.ramaElse = ramaElse
    def toAST(self):
        ramaThen = ["CaseBranch", "True", [], self.ramaThen.toAST()]
        ramaElse = ["CaseBranch", "False", [], self.ramaElse.toAST()]
        return ['ExprCase', self.condicion.toAST(), [ramaThen, ramaElse]]


def caracterEspecial(char):
    character = list(char)[1]
    if character == "t":
        parsed = 9
    elif character == 'r':
        parsed = 13
    elif character == 'n':
        parsed = 10
    else:
        parsed = ord(character)
    return parsed

def parseListString(str):
    res = []
    if len(str) == 1:
        res.append(ord(str))
    else:
        esComentario = False
        listString = list(str)[1:-1]
        for ch in listString:
            if esComentario:
                res.append(caracterEspecial(f'\\{ch}'))
                esComentario = False
            elif ch == '\\':
                esComentario = True
            else:
                res.append(ord(ch))
                esComentario = False
    return res
