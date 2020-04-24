"""
SLU-C Abstract Syntax Trees
An abstract syntax tree (AST) is a data structure that represents
the concrete (text) syntax of a program
Using a class hierarchy to represent language features in the grammar
is called the "interpreter pattern"
Singleton
Strategy Pattern  (sorting strategy)
Interpreter Pattern
design patterns - catalog of best practices in software design
"""
from typing import Sequence, Union, Optional
# Expr, Statements, FunctionDef,Pram
class Expr:
    def __init__(self,left,right):
        self.left=left
        self.right=right
    def __str__(self):
        return "{} || {}".format(self.left, self.right)


class Statement:
    def __init__(self, stmt, tabs = ""):
        self.left = stmt
        self.tabs = tabs
    def __str__(self):
        return "{}{}\n".format(self.tabs, str(self.left))

class Param:
    def __init__(self, left:str, right:Expr, args = None):
        self.left=left
        self.right=right
        self.args = args

    def __str__(self):
        if not self.left:
            return ""

        if self.args:
            params =""
            for arg in self.args:
                if type(arg) == str:
                    params += ", " + str(arg)
                else:
                    params += " " + str(arg)

            return "{0} {1}{2}".format((str(self.left)), str(self.right), params)
        return "{0} {1}".format(str(self.left), str(self.right))


class Declaration:
    def __init__(self, left: str, right: Expr, tabs =""):
        self.left = left
        self.right = right
        self.tabs = tabs
    def __str__(self):
        return "{0}{1} {2};\n".format(self.tabs, self.left, str(self.right))


class FunctionDef:
    def __init__(self, type: str, id: Expr, params: Param, decls: Declaration, stmts: Statement):
        self.type = type
        self.id = id
        self.params = params
        self.decls = decls
        self.stmts = stmts

    def __str__(self):
        declstr =""
        stmtstr = ""
        for d in self.decls:
            declstr += str(d)
        for i in range(0, len(self.stmts)):
            if i == len(self.stmts) - 1:
                stmtstr += str(self.stmts[i])
            else:
                stmtstr += str(self.stmts[i])
        return "{0} {1} ({2}) {{\n{3}{4}}}".format(self.type, str(self.id),str(self.params),declstr,stmtstr)


class Program:
    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        alist = list(map(str, self.funcs))
        strs = ""
        for f in alist:
            strs += f +"\n\n"
        return "{}".format(strs)


class BinaryExpr(Expr):
    pass


class AndExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))


class SLUCTypeError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message

class BoolExpr(Expr):
    def __init__(self, bool: str):
        self.bool = bool

    def __str__(self):
        return "{}".format(self.bool)


class AddExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} + {1})".format(str(self.left), str(self.right))

    def scheme(self) -> str:
        """
        Return a string that represents the expression in Scheme syntax.
        e.g.,  (a + b)   -> (+ a b)
        """
        return "(+ {0} {1})".format(self.left.scheme(), self.right.scheme())

    def eval(self) -> Union[int,float]:
        # TODO environment
        return self.left.eval() +  self.right.eval()


class ConjExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))


class EqExpr(Expr):
    def __init__(self, left: Expr, right: Expr,Eqlop):
        self.left = left
        self.right = right
        self.Eqlop = Eqlop
    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), str(self.Eqlop), str(self.right))

    def scheme(self) -> str:
        """
        Return a string that represents the expression in Scheme syntax.
        e.g.,  (a + b)   -> (+ a b)
        """
        return "(== {0} {1})".format(self.left.scheme(), self.right.scheme())


class RelatExpr(Expr):
    def __init__(self, left: Expr, right: Expr, relop):
        self.left = left
        self.right = right
        self.relop = relop

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), str(self.relop), str(self.right))

    def scheme(self) -> str:
        """
        Return a string that represents the expression in Scheme syntax.
        e.g.,  (a + b)   -> (+ a b)
        """
        return "(+ {0} {1})".format(self.left.scheme(), self.right.scheme())

    def eval(self) -> Union[int,float]:
        # TODO environment
        return self.left.eval() +  self.right.eval()


class PrintStatement(Statement):
    def __init__(self, prtarg: Expr, prtargs: Expr, tabs = ""):
        self.prtarg = prtarg
        self.prtargs = prtargs
        self.tabs = tabs

    def __str__(self):
        if self.prtargs:
            args = ""
            for arg in self.prtargs:
                args += ", " + str(arg)
            return "{}print({} {})".format(self.tabs, str(self.prtarg), args)
        return "{}print({})".format(self.tabs, str(self.prtarg))


class WhileStatement(Statement):
    def __init__(self, left: Expr, right: Statement, tabs = ""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{}while {} {}".format(self.tabs, str(self.left), str(self.right))


class IfStatement(Statement):
    def __init__(self, expr: Expr, stmt: Statement, elsestmt: Statement = None, tabs = ""):
        self.expr = expr
        self.stmt = stmt
        self.elsestmt = elsestmt
        self.tabs = tabs
    def __str__(self):
        if self.elsestmt :
            return "{0}if ({1}) \n\t {2} else \n\t{3}".format(self.tabs, str(self.expr), str(self.stmt), str(self.elsestmt))
        return "{0}if({1})\n{2}".format(self.tabs, str(self.expr), str(self.stmt))


class AssignmentStatement(Statement):
    def __init__(self, left: Expr, right: Expr, tabs = ""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{}{} = {};\n".format(self.tabs, str(self.left), str(self.right))


class BlockStatement(Statement):
    def __init__(self, stmt: Statement, args: Statement, tabs= ""):
        self.left = stmt
        self.right = args
        self.tabs = tabs

    def __str__(self):
        if self.right:
            stmtargs = ""
            for arg in self.right:
                stmtargs += self.tabs + str(arg) + "\n"
            return "{{\n{} {}{}}}\n".format(str(self.left), stmtargs, self.tabs)

        return "{{\n{}{}}}\n".format(str(self.left), self.tabs)


class ReturnStatement(Statement):
    def __init__(self, expr: Expr, tabs = ""):
        self.left = expr
        self.tabs = tabs
    def __str__(self):
        return "{}return {};\n".format(self.tabs, str(self.left))



class MultExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: str):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))


class UnaryMinus(Expr):
    def __init__(self, tree: Expr):
        self.tree = tree

    def __str__(self):
        return "-({0})".format(str(self.tree))

    def scheme(self):
        return "(- {0})".format(self.tree.scheme())

    def eval(self):
        return -self.tree.eval()

class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)


class StrLitExpr(Expr):

    def __init__(self,strLit:[str, Expr]):
        self.strlit = strLit

    def __str__(self):
        return str(self.strlit)


class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = float(floatlit)

    def __str__(self):
        return str(self.floatlit)

class FuncCExpr(Expr):
    def __init__(self, left: Expr, right: Sequence[FunctionDef]):
        self.left = left
        self.right = right

    def __str__(self):
        if self.right:
            args = ""
            for arg in self.right:
                args += str(arg)
            return "{0}({1})".format(str(self.left), args)
        return "{0}()".format(str(self.left))


class ExpoExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({} ** {})".format(str(self.left), str(self.right))

if __name__ == '__main__':
    """
    Represent a + b + c * d
    ((a + b) + (c * d))
    """
    expr = AddExpr(AddExpr(IDExpr('a'), IDExpr('b')),
                   MultExpr(IDExpr('c'), IDExpr('d')))
    print(expr)