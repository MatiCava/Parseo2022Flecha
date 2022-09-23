class ExprPrograma:
    def __init__(self) -> None:
        pass
        
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
        return []

class ExprString:
    def __init__(self, value) -> None:
        pass

class ExprApply:
    def __init__(self, exp1, exp2) -> None :
        self.exp1 = exp1
        self.exp2 = exp2
