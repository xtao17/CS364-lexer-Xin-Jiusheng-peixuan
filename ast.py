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
        return "({} || {})".format(self.left, self.right)

class Type:
    pass

class IntegerType(Type):
    pass

class FloatType(Type):
    pass

class BoolType(Type):
    pass

class Statement:
    def __init__(self, stmt, tabs = ""):
        self.left = stmt
        self.tabs = tabs

    def __str__(self):
        return "{}{}\n".format(self.tabs, str(self.left))

    def eval(self):
        self.left.eval()

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
    def __init__(self, type: str, id: Expr, params: Param, decls: Sequence[Declaration], stmts: Sequence[Statement]):
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

    def eval(self) -> Union[int, float, bool]:
        # an environment maps identifiers to values
        # parameters or local variables
        # to evaluate a function you evaluate all of the statements
        # within the environment
        env = {}   # TODO Fix this
        for s in self.stmts:
            s.eval(env)  # TODO define environment
class Program:
    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        alist = list(map(str, self.funcs))
        strs = ""
        for f in alist:
            strs += f +"\n\n"
        return "{}".format(strs)




class PrintStatement(Statement):
    def __init__(self, prtarg: Expr, prtargs: Sequence[Expr], tabs = ""):
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

    def eval(self, env):
        while self.left.eval():
            self.right.eval(env)


class IfStatement(Statement):
    def __init__(self, expr: Expr, stmt: Statement, elsestmt: Statement = None, tabs = ""):
        self.expr = expr
        self.stmt = stmt
        self.elsestmt = elsestmt
        self.tabs = tabs
    def __str__(self):
        if self.elsestmt :
            return "{0}if ({1})\n\t{2} else \n\t{3}".format(self.tabs, str(self.expr), str(self.stmt), str(self.elsestmt))
        return "{0}if({1})\n\t{2}".format(self.tabs, str(self.expr), str(self.stmt))

    def eval(self, env):

        if self.expr.eval():
            self.stmt.eval(env)
        elif self.elsestmt is not None:
            self.elsestmt.eval(env)


class AssignmentStatement(Statement):
    def __init__(self, left: Expr, right: Expr, tabs = ""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{0}{1} = {2};\n".format(self.tabs, str(self.left), str(self.right))


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
            return "{2}{{\n{0} {1}{2}}}\n".format(str(self.left), stmtargs, self.tabs)

        return "{1}{{\n{0}{1}}}\n".format(str(self.left), self.tabs)


class ReturnStatement(Statement):
    def __init__(self, expr: Expr, tabs = ""):
        self.left = expr
        self.tabs = tabs

    def __str__(self):
        return "{}return {};\n".format(self.tabs, str(self.left))

    def eval(self):
        return self.left.eval()


class BinaryExpr(Expr):
    pass





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

    def eval(self) -> bool:
        return self.cond.eval()


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


"""class AndExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))

        # def typeof(self) -> str: # where string is 'int' or 'float' or 'bool' or 'error'
        # strings are not abstract "INT" "int" "fred"
        # Expressions have types
        # def typeof(self) -> Type:

    def typeof(self) -> Union[int, bool, float]:  #
        
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
        
        if self.left.typeof() == BoolType and self.right.typeof() == BoolType:
            return BoolType
        else:
            # type error
            raise SLUCTypeError(
                "type error on line {0}, expected two booleans got a {1} and a {2}".format(0))
"""


class ConjExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))

    def eval(self)-> Union[int, bool, float]:
        return self.left.eval() and self.right.eval()

    def typeof(self) -> Union[int, bool, float]:
        if self.left.typeof() == BoolType and self.right.typeof() == BoolType:
            return BoolType

        else:
        # type error
            raise SLUCTypeError(
                "type error on line {0}, expected two booleans got a {1} and a {2}".format(0))


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

    def eval(self)->Union[int, bool, float]:
        if self.Eqlop == "==":
            return self.left.eval() == self.right.eval()
        elif self.Eqlop == "!=":
            return self.left.eval() != self.right.eval()




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
    def __init__(self, prtarg: Expr, prtargs: Sequence[Expr], tabs = ""):
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
    def eval(self):
        for arg in self.prtargs:
            print(arg, end =" ")


class WhileStatement(Statement):
    def __init__(self, left: Expr, right: Statement, tabs = ""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{}while {} {}".format(self.tabs, str(self.left), str(self.right))

    def eval(self, env):
        while self.left.eval():
            self.right.eval(env)


class IfStatement(Statement):
    def __init__(self, expr: Expr, stmt: Statement, elsestmt: Statement = None, tabs = ""):
        self.expr = expr
        self.stmt = stmt
        self.elsestmt = elsestmt
        self.tabs = tabs
    def __str__(self):
        if self.elsestmt :
            return "{0}if ({1})\n\t{2} else \n\t{3}".format(self.tabs, str(self.expr), str(self.stmt), str(self.elsestmt))
        return "{0}if({1})\n\t{2}".format(self.tabs, str(self.expr), str(self.stmt))

    def eval(self, env):

        if self.expr.eval():
            self.stmt.eval(env)
        elif self.elsestmt is not None:
            self.elsestmt.eval(env)


class AssignmentStatement(Statement):
    def __init__(self, left: Expr, right: Expr, tabs = ""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{0}{1} = {2};\n".format(self.tabs, str(self.left), str(self.right))


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
            return "{2}{{\n{0} {1}{2}}}\n".format(str(self.left), stmtargs, self.tabs)

        return "{1}{{\n{0}{1}}}\n".format(str(self.left), self.tabs)



class ReturnStatement(Statement):
    def __init__(self, expr: Expr, tabs = ""):
        self.left = expr
        self.tabs = tabs

    def __str__(self):
        return "{}return {};\n".format(self.tabs, str(self.left))

    def eval(self):
        return self.left.eval()
class MultExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: str):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))


    def eval(self) -> Union[int,float]:
        # TODO environment
        # Implementing SLU-C multiplication using Python's multiplication
        # implmented * using mul instruction

        # If we checked type when running eval we have a "dynamically typed"
        # language

        return self.left.eval() *  self.right.eval()

class UnaryOp(Expr):
    def __init__(self, tree: Expr, op: str):
        self.tree = tree
        self.op = op

    def __str__(self):
        return "{}({})".format(self.op, str(self.tree))

    def eval(self):
        return -self.tree.eval()

class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def eval(self, env):  # a + 7
        # lookup the value of self.id. Look up where?
        # env is a dictionary
        pass

    def typeof(self, decls) -> Type:
        # TODO type decls appropriately as a dictionary type
        # look up the variable type in the declaration dictoinary
        # from the function definition (FunctionDef)
        pass


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
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

    def eval(self):
        return self.strlit   # base case


class FloatLitExpr(Expr):

    def __init__(self, floatlit: str):
        self.floatlit = float(floatlit)

    def __str__(self):
        return str(self.floatlit)

    def eval(self):
        return self.floatlit   # base case

class FuncCExpr(Expr):
    def __init__(self, f_id: str, left: Expr, right: Sequence[Expr]):
        self.f_id = f_id
        self.left = left
        self.right = right

    def __str__(self):
        if self.right:
            args = ", "
            for i in range(0, len(self.right)):
                if i == len(self.right) - 1:
                    args += str(self.right[i])
                else:
                    args += str(self.right[i]) + ", "
            return "{}({}{})".format(self.f_id, str(self.left), args)
        return "{}({})".format(self.f_id, str(self.left))



class Farg:
    def __init__(self, arg: str):
        self.farg = arg

    def __str__(self):
        return "{}".format(self.farg)

    def eval(self):
        return self.farg

class ExpoExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({} ** {})".format(str(self.left), str(self.right))

    def eval(self) -> Union[int, float]:
        # TODO environment
        # If we checked type when running eval we have a "dynamically typed"
        # language

        return self.left.eval() ** self.right.eval()

if __name__ == '__main__':
    """
    Represent a + b + c * d
    ((a + b) + (c * d))
    """
    expr = AddExpr(AddExpr(IDExpr('a'), IDExpr('b')),
                   MultExpr(IDExpr('c'), IDExpr('d')))
    print(expr)