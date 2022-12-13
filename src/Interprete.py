import copy
import json
import operator
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

class ValueOperacion():
    def __init__(self, operador):
        self._op = operador
        self._values = []
        self._skip = False

class Lista():

    def __init__(self):
        self._list = []

class Constructor():
    def __init__(self, val):
        self._val = val

class Clausura():
    def __init__(self, var, cuerpo, env):
        self._var = var
        self._cuerpo = cuerpo
        self._env = env

class FlechaInterprete():

    mapTypes = {
        'int' : int,
        'char' : str,
        'string' : str,
        'closure' : Clausura,
    }

    mapOperadores = {
        #'ADD' : operator.add,
        'OR' : 'or',
        'AND': 'and',
        'NOT': 'not',
        'EQ': 'eq'
    }

    def __init__(self, envG, envL):
        self._envG = envG
        self._envL = envL

    def isPrimitive(self, var):
        return isinstance(var, int) or isinstance(var, bool) or isinstance(var, str)

    def evaluar(self, ast):
        self.evaluarExpr(ast)
            
    def evaluarExpr(self, ast):
        expr = ast[0]
        #print(ast)
        #print(expr)
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
        elif expr == 'ExprConstructor':
            return self.evaluarConstructor(ast[1])
        elif expr == 'ExprLet':
            return self.evaluarLet(ast[1], ast[2], ast[3])
        elif expr == 'ExprLambda':
            return Clausura(ast[1], ast[2], copy.deepcopy(self._envL))
        elif expr == 'ExprCase':
            return self.evaluarCase(ast[1], ast[2])

    def evaluarConstructor(self, expr1):
        if 'Cons' in expr1 or 'Nil' in expr1:
            return Lista()
        else:
            return Constructor(expr1)

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
                print(res)
                return res
        else:
            res1 = self.evaluarExpr(expr1)
            if isinstance(res1, ValueOperacion) and res1._skip:
                res = self.evaluarOp(res1, None)
                return res
            res2 = self.evaluarExpr(expr2)
            if isinstance(res1, Clausura):
                oldL = self._envL
                self._envL = EntornoExtendido(res1._env, res1._var, res2)
                resFinal = self.evaluarExpr(res1._cuerpo)
                self._envL = oldL
                return resFinal
            if isinstance(res1, Lista):
                if isinstance(res2, Lista):
                    res1._list.extend(res2._list)
                else:    
                    res1._list.append(res2)
                return res1
            if res1 in self.mapOperadores.keys():
                valOp = ValueOperacion(res1)
                if isinstance(res2, Constructor):
                    valOp._values.append(res2._val)
                else:
                    valOp._values.append(res2)    
                if (res1 == 'OR' and res2._val == 'True') or (res1 == 'AND' and res2._val == 'False') or (res1 == 'NOT'):
                    valOp._skip = True
                if res1 == 'NOT':
                    return self.evaluarOp(valOp, None)
                else:
                    return valOp
            if isinstance(res1, ValueOperacion):
                res = self.evaluarOp(res1, res2)
                return res

    def evaluarOp(self, valOp, segRes):
        if valOp._op =='NOT':
            if valOp._values[0] == 'True':
                return Constructor('False')
            else:
                return Constructor('True')
        elif valOp._op == 'OR':
            if valOp._skip:
                return Constructor(valOp._values[0])
            else:
                return Constructor(valOp._values[0] or segRes._val)
        elif valOp._op == 'AND':
            if valOp._skip:
                return Constructor(valOp._values[0])
            else:
                return Constructor(valOp._values[0] and segRes._val)
        elif valOp._op == 'EQ':
            return Constructor(str(valOp._values[0] == segRes))

    def evaluarCase(self, constr, branches):
        resConstr = self.evaluarExpr(constr)
        for branch in branches:
            if isinstance(resConstr, Constructor) and resConstr._val == branch[1]:
                return self.evaluarExpr(branch[3])
            if isinstance(resConstr, Lista) and 'Cons' in branch[1] and len(resConstr._list) > 0:
                test = json.dumps(branch[3])
                if ('ExprVar' in test and 'x' in test) or ('ExprVar' in test and 'xs' in test): 
                    oldL = self._envL
                    self._envL = EntornoExtendido(self._envL, branch[2][0], resConstr._list.pop(0))
                    newList = Lista()
                    newList._list = copy.deepcopy(resConstr._list)
                    self._envL = EntornoExtendido(self._envL, branch[2][1], newList)
                    resultCase = self.evaluarExpr(branch[3])
                    self._envL = oldL
                else:
                    resultCase = self.evaluarExpr(branch[3])
                return resultCase

            if isinstance(resConstr, Lista) and 'Nil' in branch[1] and len(resConstr._list) == 0:
                return self.evaluarExpr(branch[3])

            if str.lower(branch[1]) in self.mapTypes.keys() and type(resConstr) is self.mapTypes[str.lower(branch[1])]:
                return self.evaluarExpr(branch[3])

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
    
    def evaluarChar(self, val):
        return chr(val)
    
    def evaluarNum(self, val):
        return val