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
    """
    Base class for expression
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "({} || {})".format(self.left, self.right)

    def eval(self, global_env, env):
        left_eval = self.left.eval(global_env, env)
        if type(left_eval) == bool:
            left = left_eval

        else:
            raise SLUCTypeError("ERROR: type error")

        if self.right:
            right_eval = self.right.eval(global_env, env)
            if type(right_eval) == bool:
                right = right_eval
            else:
                raise SLUCTypeError("ERROR: type error")
            left = left or right

        return left


class Statement:
    """
    Base class for statement
    """
    def __init__(self, stmt, tabs=""):
        self.left = stmt
        self.tabs = tabs

    def __str__(self):
        return "{}{}\n".format(self.tabs, str(self.left))

    def eval(self, global_env, env):
        if self.left == ";":
            return self.left
        self.left.eval(global_env, env)


class Param:
    """
    Parameter
    """
    def __init__(self, left: str, right: Expr, args=None):
        self.left = left    # type
        self.right = right  # id
        self.args = args    # [type id]

    def __str__(self):
        if not self.left:
            return ""
        if self.args:
            params = ""
            for arg in self.args:
                if type(arg) == str:    # arg is type now
                    params += ", " + str(arg)
                else:   # arg is id
                    params += " " + str(arg)

            return "{0} {1}{2}".format((str(self.left)), str(self.right), params)
        return "{0} {1}".format(str(self.left), str(self.right))

    def eval(self, global_env, env):
        alist = env["arg"]
        if len(alist) > 1:
            tlist = [self.left]
            ilist = [self.right]
            for arg in self.args:
                if type(arg) == str:
                    tlist.append(arg)
                else:
                    ilist.append(arg)
            for i in range(0, len(ilist)):
                env[str(ilist[i])] = (tlist[i], alist[i])
        else:
            env[str(self.right)] = ("int", (alist[0]))


class AssignmentStatement(Statement):
    def __init__(self, left: Expr, right: Expr, tabs=""):
        self.left = left    # id
        self.right = right  # value
        self.tabs = tabs

    def __str__(self):
        return "{0}{1} = {2};\n".format(self.tabs, str(self.left), str(self.right))

    def eval(self, global_env, env):
        t = env[str(self.left)][0]

        if t == "int":
            if type(self.right) == IntLitExpr:
                env.update({str(self.left): (t, int(str(self.right)))})
            elif type(self.right) == FloatLitExpr:
                env.update({str(self.left): (t, int(float(str(self.right))))})
            elif type(self.right) == StrLitExpr or type(self.right) == BoolExpr:
                raise SLUCTypeError("ERROR: Variable {} incorrect assignment type".format(self.left))
            else:
                result = self.right.eval(global_env, env)
                env.update({str(self.left): (t, int(result))})

        if t == "float":
            if type(self.right) == IntLitExpr or type(self.right) == FloatLitExpr:
                env.update({str(self.left): (t, (float(str(self.right))))})
            elif type(self.right) == StrLitExpr or type(self.right) == BoolExpr:
                raise SLUCTypeError("ERROR: Variable {} incorrect assignment type".format(self.left))
            else:
                result = self.right.eval(global_env, env)
                env.update({str(self.left): (t, float(result))})

        if t == "bool":
            if type(self.right) == BoolExpr:
                env.update({str(self.left): (t, self.right.eval(global_env, env))})
            elif type(self.right) == IntLitExpr \
                    or type(self.right) == FloatLitExpr \
                    or type(self.right) == StrLitExpr:
                raise SLUCTypeError("ERROR: Variable {} incorrect assignment type".format(self.left))
            else:
                result = self.right.eval(global_env, env)

                if type(result) == bool:
                    env.update({str(self.left): (t, result)})
                else:
                    raise SLUCTypeError("ERROR: Variable {} incorrect assignment type".format(self.left))

        if t == "str":
            if type(self.right) == StrLitExpr:
                env.update({str(self.left): (t, str(self.right.eval(global_env, env)))})
            else:
                raise SLUCTypeError("ERROR: Variable {} incorrect assignment type".format(self.left))


class Declaration:
    """
    Declaration
    """
    def __init__(self, left: str, right: Union[Expr, Statement], tabs=""):
        self.left = left    # type
        self.right = right  # id | assignment
        self.tabs = tabs

    def __str__(self):
        if type(self.right) == AssignmentStatement:
            return "{0}{1} {2}".format(self.tabs, self.left, str(self.right))
        return "{0}{1} {2};\n".format(self.tabs, self.left, str(self.right))

    def eval(self, global_env, env):
        if type(self.right) == AssignmentStatement:
            id = str(self.right)[0]
            env[id] = (self.left, None)
            self.right.eval(global_env, env)
        else:
            env[str(self.right)] = (self.left, None)  # ID: (type, value)


class FunctionDef:
    def __init__(self, ftype: str, id: Expr, params: Param, decls: Sequence[Declaration], stmts: Sequence[Statement]):
        self.type = ftype
        self.id = id
        self.params = params
        self.decls = decls
        self.stmts = stmts

    def __str__(self):
        declstr = ""
        stmtstr = ""
        for d in self.decls:
            declstr += str(d)
        for i in range(0, len(self.stmts)):
            if i == len(self.stmts) - 1:
                stmtstr += str(self.stmts[i])
            else:
                stmtstr += str(self.stmts[i])
        return "{0} {1} ({2}) {{\n{3}{4}}}".format(self.type, str(self.id), str(self.params), declstr, stmtstr)

    def eval(self, global_env, env={}) -> Union[None, int, float, bool]:
        # an environment maps identifiers to values
        # parameters or local variables
        # to evaluate a function you evaluate all of the statements
        # within the environment
        # id: (type, params, decls, stmts)

        if str(self.id) in global_env:
            self.params.eval(global_env, env)   # get the value of a param
            for d in self.decls:
                d.eval(global_env, env)

            for s in self.stmts:
                if type(s) in {ReturnStatement, IfStatement}:
                    if str(type(s.eval(global_env, env)).__name__) == self.type:
                        return s.eval(global_env, env)
                    else:
                        raise SLUCTypeError("ERROR: type error")
                else:
                    s.eval(global_env, env)

        elif str(self.id) == "main":
            env = {}
            for d in self.decls:
                d.eval(global_env, env)
            for s in self.stmts:
                s.eval(global_env, env)

        else:
            global_env[str(self.id)] = (self.type, FunctionDef(self.type, self.id, self.params, self.decls, self.stmts))
        return None


class Program:
    def __init__(self, funcs: Sequence[FunctionDef]):
        self.funcs = funcs

    def __str__(self):
        alist = list(map(str, self.funcs))
        strs = ""
        for f in alist:
            strs += f + "\n\n"
        return "{}".format(strs)

    def eval(self):
        env_func = {}
        for func in self.funcs:
            func.eval(env_func)


class BinaryExpr(Expr):
    pass


class SLUCTypeError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class AddExpr(BinaryExpr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} + {1})".format(str(self.left), str(self.right))

    def eval(self, global_env, env) -> Union[int, float]:
        if type(self.left) == IDExpr:
            left = self.left.eval(global_env, env)
        else:
            left = self.left.eval(global_env, env)
        if type(self.right) == IDExpr:
            right = self.right.eval(global_env, env)
        elif type(self.right) == IntLitExpr:

            right = self.right.eval()
        else:
            right = self.right.eval(global_env, env)
        if type(left) == bool or type(right) == bool:
            raise SLUCTypeError("ERROR: type error")
        return left + right


class MultExpr(BinaryExpr):
    def __init__(self, left: Expr, right: Expr, op: str):
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))

    def eval(self, global_env, env) -> Union[int, float]:
        left = self.left.eval(global_env, env)
        right = self.right.eval(global_env, env)
        if self.op == "*":
            return left * right
        elif self.op == "/":
            return left / right
        else:
            return left % right


class ExpoExpr(BinaryExpr):
    """
    Represents exponential operation
    """
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({} ** {})".format(str(self.left), str(self.right))

    def eval(self, global_env, env) -> Union[int, float]:
        # TODO environment
        # If we checked type when running eval we have a "dynamically typed"
        # language
        if type(self.left) == IDExpr:
            left = self.left.eval(global_env, env)
        else:
            left = self.left.eval()
        if type(self.right) == IDExpr:
            right = self.right.eval(global_env, env)
        elif type(self.right) == IntLitExpr:

            right = self.right.eval()
        else:
            right = self.right.eval(global_env, env)
        return left ** right


class ConjExpr(BinaryExpr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} && {1})".format(str(self.left), str(self.right))

    def eval(self, global_env, env) -> Union[int, bool, float]:
        left_eval = self.left.eval(global_env, env)
        if type(left_eval) == bool:
            left = left_eval
        else:
            raise SLUCTypeError("ERROR: type error")

        if self.right:
            right_eval = self.right.eval(global_env, env)
            if type(right_eval) == bool:
                right = right_eval
            else:
                raise SLUCTypeError("ERROR: type error")
            left = left and right

        return left


class EqExpr(BinaryExpr):
    def __init__(self, left: Expr, right: Expr, Eqlop):
        self.left = left
        self.right = right
        self.Eqlop = Eqlop

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), str(self.Eqlop), str(self.right))

    def eval(self, global_env, env) -> Union[int, bool, float]:
        if self.Eqlop == "==":
            return self.left.eval(global_env, env) == self.right.eval(global_env, env)
        else:
            return self.left.eval(global_env, env) != self.right.eval(global_env, env)


class RelatExpr(BinaryExpr):
    def __init__(self, left: Expr, right: Expr, relop):
        self.left = left
        self.right = right
        self.relop = relop

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), str(self.relop), str(self.right))

    def eval(self, global_env, env) -> Union[int, float]:
        # TODO environment
        if self.right:
            if self.relop == "<":
                return self.left.eval(global_env, env) < self.right.eval(global_env, env)
            elif self.relop == "<=":
                return self.left.eval(global_env, env) <= self.right.eval(global_env, env)
            elif self.relop == ">":
                return self.left.eval(global_env, env) > self.right.eval(global_env, env)
            elif self.relop == ">=":
                return self.left.eval(global_env, env) >= self.right.eval(global_env, env)
        return self.left.eval(global_env, env)


class PrintStatement(Statement):
    def __init__(self, prtarg: Expr, prtargs: Sequence[Expr], tabs=""):
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

    def eval(self, global_env, env):
        if self.prtargs:
            print(self.prtarg.eval(global_env, env), end=" ")
            for i in range(0, len(self.prtargs)):
                if i == len(self.prtargs) - 1:
                    print(self.prtargs[i].eval(global_env, env))
                else:
                    print(self.prtargs[i].eval(global_env, env), end=" ")
        else:
            print(self.prtarg.eval(global_env, env))


class WhileStatement(Statement):
    def __init__(self, left: Expr, right: Statement, tabs=""):
        self.left = left
        self.right = right
        self.tabs = tabs

    def __str__(self):
        return "{}while {} {}".format(self.tabs, str(self.left), str(self.right))

    def eval(self, global_env, env):
        while self.left.eval(global_env, env):
            self.right.eval(global_env, env)


class IfStatement(Statement):
    def __init__(self, expr: Expr, stmt: Statement, elsestmt: Statement = None, tabs=""):
        self.expr = expr
        self.stmt = stmt
        self.elsestmt = elsestmt
        self.tabs = tabs

    def __str__(self):
        if self.elsestmt:
            return "{0}if ({1})\n\t{2} else \n\t{3}".format(self.tabs, str(self.expr),
                                                            str(self.stmt), str(self.elsestmt))
        return "{0}if({1})\n\t{2}".format(self.tabs, str(self.expr), str(self.stmt))

    def eval(self, global_env, env):
        if self.expr.eval(global_env, env):
            return self.stmt.eval(global_env, env)
        elif self.elsestmt:
            return self.elsestmt.eval(global_env, env)
        return None


class BlockStatement(Statement):
    def __init__(self, stmt: Statement, args: Sequence[Statement], tabs=""):
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

    def eval(self, global_env, env):
        self.left.eval(global_env, env)
        for argument in self.right:
            argument.eval(global_env, env)


class ReturnStatement(Statement):
    def __init__(self, expr: Expr, tabs=""):
        self.left = expr
        self.tabs = tabs

    def __str__(self):
        return "{}return {};\n".format(self.tabs, str(self.left))

    def eval(self, global_env, env):
        return self.left.eval(global_env, env)


class UnaryOp(Expr):
    def __init__(self, tree: Expr, op: str):
        self.tree = tree
        self.op = op

    def __str__(self):
        return "{}({})".format(self.op, str(self.tree))

    def eval(self, global_env, env):
        if self.op == "-":
            return -self.tree.eval(global_env, env)
        else:
            return not self.tree.eval(global_env, env)


class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def eval(self, global_env, env):  # a + 7
        return env[self.id][1]


class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def eval(self, global_env={}, env={}) -> int:
        return self.intlit   # base case


class StrLitExpr(Expr):

    def __init__(self, strlit: str):
        self.strlit = strlit

    def __str__(self):
        return str(self.strlit)

    def eval(self, global_env={}, env={}) -> str:
        return self.strlit   # base case


class FloatLitExpr(Expr):
    def __init__(self, floatlit: str):
        self.floatlit = float(floatlit)

    def __str__(self):
        return str(self.floatlit)

    def eval(self, global_env={}, env={}) -> float:
        return self.floatlit   # base case


class BoolExpr(Expr):
    def __init__(self, bool: str):
        self.bool = bool

    def __str__(self):
        return "{}".format(self.bool)

    def eval(self, global_env={}, env={}) -> bool:
        if self.bool == "true":
            return True
        else:
            return False


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

    def eval(self, global_env, env) -> Union[int, float, bool]:

        if self.right:
            args = [self.left.eval(global_env, env)]
            for a in self.right:
                args.append(a.eval(global_env, env))
            return global_env[str(self.f_id)][1].eval(global_env, {"arg": args})

        else:
            return global_env[str(self.f_id)][1].eval(global_env, {"arg": [self.left.eval(global_env, env)]})


class Farg(Expr):
    """
    Represents function arguments
    """
    def __init__(self, arg: Expr):
        self.farg = arg

    def __str__(self):
        return "{}".format(str(self.farg))

    def eval(self, global_env, env) -> Union[int, float, bool]:
        return self.farg.eval(global_env, env)


if __name__ == '__main__':
    """
    Represent a + b + c * d
    ((a + b) + (c * d))
    """
    globalenv = {"b": ("int", 2)}
    env = {"a": ("int", 1)}
    expr = AddExpr(IDExpr("a"), IntLitExpr("2"))
    assignment = AssignmentStatement(IDExpr("c"), IntLitExpr("3"))
    print(assignment.eval({}, {"c": ("int", None)}))
    print(expr.eval({}, env))
