class EntornoVacio():
    def __init__(self):
        pass

    def lookup(self, var):
        raise Exception("Variable no esta ligada")
        #print("Variable no esta ligada")

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
        #en test 10 quedamos con una definicion en glob de x 42
        #mientras que en local estamos definiedo una x con 43
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
        elif expr == 'ExprLambda':
            return self.evaluarLamb(ast[1], ast[2])
#con unsafe print es imprimir en el momento o es guardar resultado e imprimir al final, porque test hola mundo depende de esto
#y test que pisa x e imprime 42 44 42 tambien dependen
    def evaluarApply(self, expr1, expr2):
        if expr1[0] == 'ExprVar':
            if 'unsafePrint' in expr1[1]:
                res = self.evaluarExpr(expr2)
                print('RESULT UNSAFE PRINT')
                print(res)
                return res
        if expr1[0] == 'ExprLambda':
            return self.evaluarLamb(expr1, expr2)

    def evaluarVar(self, expr):
        try:
            return self._envL.lookup(expr)
        except:
            return self._envG[expr]

#prguntar test 5 resultado de main queda salto de linea solo y en local queda hola mundo
    def evaluarLet(self, var, val, aplicacion):
        try:
            #pisamos locales? o como se maneja? en caso 07 se nos esta sumando creo y para strings como el 05 si el print
            #tenemos que juntar resultado todo en env y despues imprimir si tendriamos que concatenar
            #de una forma similar como ahora
            #valLocal = self._envL.lookup(var)
            #self._envL = EntornoExtendido(self._envL, var, valLocal + self.evaluarExpr(val))
            self._envL = EntornoExtendido(self._envL, var, self.evaluarExpr(val))
        except:
            self._envL = EntornoExtendido(self._envL, var, self.evaluarExpr(val))
        return self.evaluarExpr(aplicacion)      

    def evaluarLamb(self, expr1, expr2):
        #pisamos locales? o como se maneja?
        self._envL = EntornoExtendido(self._envL, expr1[1], self.evaluarExpr(expr2))
        return self.evaluarExpr(expr1[2])

    def evaluarChar(self, val):
        return chr(val)
    
    def evaluarNum(self, val):
        return val