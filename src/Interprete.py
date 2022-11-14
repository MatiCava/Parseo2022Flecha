class EntornoVacio():
    def __init__(self):
        pass

    def lookup(self, var):
        raise Exception("Variable no esta ligada")

class EntornoExtendido():
    def __init__(self, env, var, val):
        self._env = env
        self._var = var
        self._val = val

    def lookup(self, var):
        if var == self._var:
            return self._val
        else:
            return self._env.lookup(var)

class FlechaInterprete():
    def __init__(self, envG, envL):
        self._envG = envG
        self._envL = envL

    def isPrimitive(self, var):
        return isinstance(var, int) or isinstance(var, bool) or isinstance(var, str)

    def evaluar(self, ast):
        self.evaluarExpr(ast)
            
    def evaluarExpr(self, ast):
        expr = ast[0]
        print(ast)
        print(expr)
        if expr == 'Def':
            self._envG[ast[1]] = self.evaluarExpr(ast[2])
        elif expr == 'ExprApply':
            return self.evaluarApply(ast[1], ast[2])
        elif expr == 'ExprVar':
            return self.evaluarVar(ast[1])
        elif expr == 'ExprChar':
            return self.evaluarChar(ast[1])
        elif expr == 'ExprNumber':
            return self.evaluarNum(ast[1])

#aca em apply deberia guardar nueva variable o en evaluar var o solo guardar incognito con un let?
    def evaluarApply(self, expr1, expr2):
        if expr1[0] == 'ExprVar':
            if 'unsafePrint' in expr1[1]:
                return self.evaluarExpr(expr2)
        #idea de extender env cuando guardamos    
        #self._envL = EntornoExtendido(self._envL, self.evaluarVar(expr1[1]), self.evaluarExpr(expr2))

#que deberia hacer buscar y si no esta guardar? donde terminamos imprimiendo
    def evaluarVar(self, expr):
        try:
            return self._envL.lookup(expr)
        except:
            return self._envG[expr]

    def evaluarChar(self, val):
        return chr(val)
    
    def evaluarNum(self, val):
        return val