import copy
import sys


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

class Clausura():
    def __init__(self, var, cuerpo, env):
        self._var = var
        self._cuerpo = cuerpo
        self._env = env

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
            return Clausura(ast[1], ast[2], copy.deepcopy(self._envL))

    def evaluarApply(self, expr1, expr2):
        if expr1[0] == 'ExprVar' and ('unsafePrintInt' in expr1[1] or 'unsafePrintChar' in expr1[1]):
            if 'unsafePrintInt' in expr1[1]:
                res = self.evaluarExpr(expr2)
                print('RESULT UNSAFE PRINT INT')
                print(res)
                return res
            if 'unsafePrintChar' in expr1[1]:
                res = self.evaluarExpr(expr2)
                print('RESULT UNSAFE PRINT CHAR')
                sys.stdout.write(res)
                return res
        else:
            res1 = self.evaluarExpr(expr1)
            res2 = self.evaluarExpr(expr2)
            if isinstance(res1, Clausura):
                self._envL = EntornoExtendido(self._envL, res1._var, res2)
                resFinal = self.evaluarExpr(res1._cuerpo)
                return resFinal

    def evaluarVar(self, expr):
        try:
            return self._envL.lookup(expr)
        except:
            return self._envG[expr]

    def evaluarLet(self, var, val, aplicacion):
        oldL = self._envL
        self._envL = EntornoExtendido(self._envL, var, self.evaluarExpr(val))
        res = self.evaluarExpr(aplicacion)
        self._envL = oldL
        return res

    def evaluarLamb(self, expr1, expr2):
        self._envL = EntornoExtendido(self._envL, expr1[1], self.evaluarExpr(expr2))
        return self.evaluarExpr(expr1[2])

    def evaluarChar(self, val):
        return chr(val)
    
    def evaluarNum(self, val):
        return val