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
        #esta bien solo guardar global con def?
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
        elif expr == 'ExprLet':
            return self.evaluarLet(ast[1], ast[2], ast[3])

    def evaluarApply(self, expr1, expr2):
        if expr1[0] == 'ExprVar':
            if 'unsafePrint' in expr1[1]:
                res = self.evaluarExpr(expr2)
                print('RESULT UNSAFE PRINT')
                print(res)
                return res
        if expr1[0] == 'ExprLambda':
            #pisamos locales? o como se maneja?
            self._envL = EntornoExtendido(self._envL, expr1[1], self.evaluarExpr(expr2))

    def evaluarVar(self, expr):
        try:
            return self._envL.lookup(expr)
        except:
            return self._envG[expr]

#prguntar test 5 resultado de main queda salto de linea solo y en local queda hola mundo
    def evaluarLet(self, var, val, aplicacion):
        try:
            #pisamos locales? o como se maneja?
            valLocal = self._envL.lookup(var)
            self._envL = EntornoExtendido(self._envL, var, valLocal + self.evaluarExpr(val))
        except:
            self._envL = EntornoExtendido(self._envL, var, self.evaluarExpr(val))
        return self.evaluarExpr(aplicacion)      

    def evaluarChar(self, val):
        return chr(val)
    
    def evaluarNum(self, val):
        return val