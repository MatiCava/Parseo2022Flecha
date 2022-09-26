class Programa:
    def __init__(self) -> None:
        self.defs = []
        
    def addDef(self, value) -> None:
        self.defs.append(value)
        
class ExprDefinicion:
    def __init__(self, id, parametros, expresion) -> None:
        self.id = id

class ExprChar:
    def __init__(self, value) -> None:
        return ['ExprChar', parseASCII(value)] 

class ExprVar:
    def __init__(self, id) -> None:
        return ['ExprVar', id]

class ExprNumber:
    def __init__(self, value) -> None:
        return ['ExprVar', int(value)]

class ExprConstructor:
    def __init__(self, id) -> None:
        return ['ExprConstructor', id]
        
class ExprEmpty:
    def __init__(self) -> None:
        self.expr = []
    
    def toAST(self) -> None:
        return self.expr

class ExprString:
    def __init__(self, value) -> None:
        pass

class ExprApply:
    def __init__(self, exp1, exp2) -> None :
        self.exp1 = exp1
        self.exp2 = exp2
        
    def toAST(self) -> None:
        return ['ExprApply', self.exp1.toAST(), self.exp2.toAST()]
    
