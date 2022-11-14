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
            self._envG[ast[1]] = self.evaluar(ast[2])
        elif expr == 'ExprApply':
            self.evaluarApply(ast[1], ast[2])
        elif expr == 'ExprVar':
            self.evaluarVar(ast[1])
        elif expr == 'ExprChar':
            self.evaluarChar(ast[1])

#aca em apply deberia guardar nueva variable o en evaluar var?
    def evaluarApply(self, expr1, expr2):
        if expr1[0] == 'ExprVar':
            self._envL = EntornoExtendido(self._envL, self.evaluarVar(expr1[1]), self.evaluarExpr(expr2))
#que deberia hacer buscar y si no esta guardar? donde terminamos imprimiendo
    def evaluarVar(self, expr, expr2):
        testPrint
        try:
            testPrint = self._envL.lookup(expr)
        except:
            testPrint = self._envG[expr]

        if 'unsafePrint' in expr:
            print(testPrint)

    def evaluarChar(self, val):
        return chr(val)