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

# Use a class hierarchy to represent types.
class Expr:
    """
    Base class for expressions
    """
    """
      Base class for expressions
      """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "{} || {}".format(self.left, self.right)


class FunctionDef:
    def __init__(self, type: str, id: Expr, params: Expr, decls: Expr, stmts: Expr):
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
        for s in self.stmts:
            stmtstr += str(s)
        return "{} {} ({}) {{{}{}}}".format(self.type, str(self.id),str(self.params),declstr,stmtstr)



class ParamExpr(Expr):
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


class Program:

    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        alist = list(map(str, self.funcs))
        strs = ""
        for f in alist:
            strs += f
        return "{}".format(strs)

# TODO Don't just cut-and-paste new operations, abstract!

class BinaryExpr(Expr):
    pass

class AndExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))


    # def typeof(self) -> str: # where string is 'int' or 'float' or 'bool' or 'error'
    # strings are not abstract "INT" "int" "fred"
    # Expressions have types
    #def typeof(self) -> Type:
    def typeof(self) -> Union[int, bool, float]:   #
        """
        Return the type of the expression.
        1) 4 + 4 is an int
        2) 2 * 3.14 is a float
        3) True && False is a bool
        4) True && 3.14 type error
        Static type checking: type check the program *before* we evaluate it.
        Scheme is dynamically type checked. Type errors checked at run time.
        Java - statically type checked.
        C - static
        Python - dynamic, checked at run time
                 mypy - static type checker for Python
        """
        if self.left.typeof() == BoolType and self.right.typeof() == BoolType:
            return BoolType
        else:
            # type error
            raise SLUCTypeError(
                "type error on line {0}, expected two booleans got a {1} and a {2}".format(0))

class SLUCTypeError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message

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


class DecExpr(Expr):
    def __init__(self, left: str, right: Expr):
        self.left = left
        self.right = right
    def __str__(self):
        return "{0} {1};".format(self.left, str(self.right))



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


class PrintStmtExpr(Expr):
    def __init__(self, prtarg: Expr, prtargs: Expr):
        self.prtarg = prtarg
        self.prtargs = prtargs

    def __str__(self):
        if self.prtargs:
            args = ""
            for arg in self.prtargs:
                args += ", " + str(arg)
            return "print({} {})\n".format(str(self.prtarg), args)
        return "print({})\n".format(str(self.prtarg))


class WhileExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "while( {} ) {}".format(str(self.left), str(self.right))


class IfExpr(Expr):
    def __init__(self, expr: Expr, stmt: Expr, elsestmt: Expr = None):
        self.expr = expr
        self.stmt = stmt
        self.elsestmt = elsestmt
    def __str__(self):
        if self.elsestmt :
            return "if ({0}) {1} \n else {2}".format(str(self.expr), str(self.stmt), str(self.elsestmt))
        return "if({0}) {1}".format(str(self.expr), str(self.stmt))


class AssignmentExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "{} = {};\n".format(str(self.left), str(self.right))


class BlockExpr(Expr):
    def __init__(self, stmt: Expr, args: Expr):
        self.stmt = stmt
        self.args = args

    def __str__(self):
        if self.args:
            stmtargs = ""
            for arg in self.args:
                stmtargs += "\n" + str(arg)
            return "{{\n{0} {1}}}".format(str(self.stmt), stmtargs)

        return "{{\n{0}}}\n".format(str(self.stmt))


class ReturnExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def __str__(self):
        return "return {};".format(str(self.expr))

class StmtExpr(Expr):
    def __init__(self, stmt):
        self.stmt = stmt

    def __str__(self):
        return "{}".format(str(self.stmt))


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

    def scheme(self):
        return self.id

    def eval(self, env):  # a + 7
        # lookup the value of self.id. Look up where?
        # env is a dictionary
        pass

class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def scheme(self):
        return str(self.intlit)

    def eval(self):
        return self.intlit   # base case

    #def typeof(self) -> Type:
    # representing SLU-C types using Python types
    def typeof(self) -> type:

        #return IntegerType
        return int

class StrLitExpr(Expr):

    def __init__(self,strLit:[str, Expr]):
        self.strlit = strLit

    def __str__(self):
        return str(self.strlit)

    def scheme(self):
        return str(self.strlit)

    def eval(self):
        return self.strlit

    def typeof(self) -> type:

        #retrurn String type
        return str

class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = float(floatlit)

    def __str__(self):
        return str(self.floatlit)

    def scheme(self):
        return str(self.floatlit)

    def eval(self):
        return self.floatlit   # base case

    #def typeof(self) -> Type:
    # representing SLU-C types using Python types
    def typeof(self) -> type:

        #return FloatType
        return float

if __name__ == '__main__':
    """
    Represent a + b + c * d
    ((a + b) + (c * d))
    """
    expr = AddExpr(AddExpr(IDExpr('a'), IDExpr('b')),
                   MultExpr(IDExpr('c'), IDExpr('d')))
    print(expr)