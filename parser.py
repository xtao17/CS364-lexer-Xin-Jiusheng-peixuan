"""
Xin, Jiusheng, Peixuan

"""
from lexer import Lexer
from ast import *
import sys


class Parser:
    """
        Parser class is used to implement SLUC grammar
    """
    def __init__(self, fn: str):
        #  list for checking variable id and function id
        self.var_id = []
        self.func_id = []
        self.level = 0
        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.currtok = next(self.tg)
        #  expression dictionary for DRY rule
        self.ex_dict = {
            "real": (lambda x: FloatLitExpr(x)),
            "int": (lambda x: IntLitExpr(x))
        }
        #  Statement dictionary for DRY rule
        self.stmt_dict = {
            "if": (lambda x: self.ifstatement()),
            "while": (lambda x: self.whilestatement()),
            "print": (lambda x: self.printstmt()),
            "return": (lambda x: self.returnstmt()),
            "ID": (lambda x: self.assignment())
         }

    # function for create a \t based on level
    def formctrl(self) -> str:
        return "\t"*self.level

    # function to check whether id exists or not
    def check_id_exist(self,var_name,id_list):
        if var_name not in id_list:
            return False
        return True

    def program(self) -> Program:
        funcdefs = []
        #   append functions until the end of file
        while self.currtok and self.currtok.name != "EOF":
            funcdefs.append(self.functiondef())

        return Program(funcdefs)

    def functiondef(self) -> FunctionDef:
        stms = []
        decs = []
        currentline = self.currtok.loc
        self.level = 0
        self.var_id.clear()
        #  check type
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            type = self.currtok.name
            self.currtok = next(self.tg)
            # check id
            if self.currtok.kind == "ID" or (self.currtok.kind=="Keyword" and self.currtok.name=="main"):
                if self.check_id_exist(self.currtok.name,self.func_id):
                    raise SLUCSyntaxError("ERROR: ID {} duplicated on line {}".format(self.currtok.name,self.currtok.loc))
                self.func_id.append(self.currtok.name)
                id=IDExpr(self.currtok.name)
                # add id to parameter list
                self.currtok = next(self.tg)
                # dealing with parameters
                if self.currtok.kind == "left-paren":
                    self.currtok = next(self.tg)
                    parm = self.params()
                    if self.currtok.kind == "right-paren":
                        self.currtok = next(self.tg)
                # dealing with braces
                    if self.currtok.kind == "left-brace":
                        self.level += 1
                        self.currtok = next(self.tg)
                        while(self.currtok.name in {"int", "bool", "float"}):
                            decs.append(self.declaration())
                        while(self.currtok.kind != "right-brace"):
                            stms.append(self.statement())
                            if self.currtok.name in  {"int", "bool", "float"}:
                                raise SLUCSyntaxError("ERROR: declarations must be written before statements on line {}".format(self.currtok.loc))

                        self.currtok = next(self.tg)
                        return FunctionDef(type, id, parm, decs, stms)

        raise SLUCSyntaxError("ERROR: Invalid function definition on line {}".format(currentline))

    def params(self) -> Param:
        args =[]
        if self.currtok.kind == "Keyword" and self.currtok.name in{"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                self.var_id.append(self.currtok.name)
                right = IDExpr(self.currtok.name)
                self.currtok = next(self.tg)
            else:
                raise SLUCSyntaxError("ERROR: Invalid param on line {}".format(self.currtok.loc))

            while (self.currtok.kind == "comma"):
                self.currtok = next(self.tg)
                type=self.currtok.name
                args.append(self.currtok.name)
                self.currtok = next(self.tg)
                args.append(IDExpr(self.currtok.name))
                self.var_id.append(self.currtok.name)
                self.currtok = next(self.tg)
            return Param(left, right, args)

        elif self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            return Param("", "")

        raise SLUCSyntaxError("ERROR: Invalid param on line {}".format(self.currtok.loc))

    def declaration(self) -> Declaration:
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                #  add id
                if not self.check_id_exist(self.currtok.name, self.var_id):
                    self.var_id.append(self.currtok.name)
                    right = IDExpr(self.currtok.name)
                    self.currtok = next(self.tg)
                else:
                    raise SLUCSyntaxError("ERROR: ID {} duplicated on line {}".format(self.currtok.name, self.currtok.loc))
            else:
                raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok))
            if self.currtok.kind=="semicolon":
                self.currtok = next(self.tg)
                return Declaration(left, right, self.formctrl())
        raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok.loc))

    def statement(self) -> Statement:
        if self.currtok.kind == "semicolon":  # using ID in expression
            tmp = self.currtok
            self.currtok = next(self.tg)
            return Statement(tmp.name)
        if self.currtok.kind == "left-brace":
            return self.block()

        if self.currtok.kind == "Keyword":
            item=self.stmt_dict[self.currtok.name](self)
            return item

        if self.currtok.kind == "ID":
            item=self.stmt_dict[self.currtok.kind](self)
            return item

        raise SLUCSyntaxError("ERROR: Invalid statement {} on line {}".format(self.currtok.name, self.currtok.loc))

    def returnstmt(self) -> Statement:
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        expr = self.expression()
        if self.currtok.kind == "semicolon":
            self.currtok = next(self.tg)
            return ReturnStatement(expr, self.formctrl())
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(currentline))

    def block(self) -> Statement:
        stmts = []
        self.currtok = next(self.tg)
        stmt = self.statement()
        while self.currtok.kind != "right-brace":
            stmts.append(self.statement())
        self.currtok = next(self.tg)
        return BlockStatement(stmt, stmts, self.formctrl())

    def assignment(self) -> Statement:
        currentline = self.currtok.loc
        if self.check_id_exist(self.currtok.name,self.var_id):
            id = IDExpr(self.currtok.name)
        else:
            raise SLUCSyntaxError("ERROR: Variable {} not defined on line {}".format(self.currtok.name, self.currtok.loc))
        self.currtok = next(self.tg)
        if self.currtok.kind == "assignment":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "semicolon":
                self.currtok = next(self.tg)
                assign = AssignmentStatement(id, expr, self.formctrl())
                return assign
        raise SLUCSyntaxError("ERROR: Invalid Assignment on line {}".format(currentline))

    def ifstatement(self) -> Statement:
        self.level += 1
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        #  dealing with conditions
        if self.currtok.kind == "left-paren":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "right-paren":
                self.currtok = next(self.tg)
                stmt = self.statement()
                if self.currtok.kind == "Keyword" and self.currtok.name == "else":
                    self.currtok = next(self.tg)
                    elsestmt = self.statement()
                    ifstmt = IfStatement(expr, stmt, elsestmt, self.formctrl())
                    self.level -= 1
                    return ifstmt
                ifstmt = IfStatement(expr, stmt, tabs=self.formctrl())
                self.level -= 1
                return ifstmt

        raise SLUCSyntaxError("ERROR: Invalid ifstatement on line {}".format(currentline))

    def whilestatement(self) -> Statement:
        self.level += 1
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        # dealing with conditions
        if self.currtok.kind == "left-paren":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "right-paren":
                self.currtok = next(self.tg)
                stmt = self.statement()
                whilestmt = WhileStatement(expr, stmt, self.formctrl())
                self.level -= 1
                return whilestmt
        raise SLUCSyntaxError("ERROR: Invalid whilestatement on line {}".format(currentline))

    def printstmt(self) -> Statement:
        currentline = self.currtok.loc
        prtargs = []
        self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            self.currtok = next(self.tg)
            prtarg = self.printarg()
        else:
            raise  SLUCSyntaxError("ERROR: Missing ( on line {}".format(currentline))
        while (self.currtok.kind == "comma"):
            self.currtok = next(self.tg)
            prtargs.append(self.printarg())
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            left = PrintStatement(prtarg, prtargs, self.formctrl())
            return left
        raise SLUCSyntaxError("ERROR: Invalid print statement on line {}".format(currentline))

    def printarg(self) -> Expr:
        if self.currtok.kind == "String":
            tmp = self.currtok
            self.currtok = next(self.tg)
            return StrLitExpr(tmp.name)
        return StrLitExpr(self.expression())

    def expression(self) -> Expr:
        left = self.conjunction()
        while self.currtok.kind == "or":
            self.currtok = next(self.tg)
            right = self.conjunction()
            left = Expr(left, right)
        return left

    def conjunction(self) -> Expr:
        left = self.equality()

        while self.currtok.kind == "and":
            self.currtok = next(self.tg)
            right = self.equality()
            left = ConjExpr(left, right)
        return left

    def equality(self):  # a == b      3*z != 99
        left = self.relation()

        if self.currtok.kind in {"equal-equal", "not-equal"}:
            equop = self.currtok.name
            self.currtok = next(self.tg)
            right = self.relation()
            left = EqExpr(left, right, equop)
        return left

    def relation(self) -> Expr:  # a < b
        left = self.addition()
        while self.currtok.kind in {"less-than", "less-equal", "greater-than", "greater-equal"}:
            relop = self.currtok.name
            self.currtok = next(self.tg)
            right = self.addition()
            left = RelatExpr(left, right, relop)
        return left

    def addition(self) -> Expr:
        """
        Expr  →  Term { + Term }
        """

        left = self.term()

        while self.currtok.kind in {"plus", "minus"}:
            if self.currtok.kind == "plus":
                self.currtok = next(self.tg)  # advance to the next token

            # because we matched a +
            right = self.term()
            left = AddExpr(left, right)

        return left

    def funcC(self, f_id) -> Expr:
        """
        FuncC → id (farg {, farg})
         """
        left = self.farg()
        args = []
        while self.currtok.kind == "comma":
            self.currtok = next(self.tg)
            args.append(self.farg())
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            left = FuncCExpr(f_id, left, args)
            return left

        raise SLUCSyntaxError("ERROR: Invalid function call on line {}".format(self.currtok.loc))

    def farg(self) -> Farg:
        """
        Farg → id | intlit | float | epsilon
        """
        if self.currtok.kind == "ID":
            if self.check_id_exist(self.currtok.name, self.var_id):
                tmp = self.currtok
                self.currtok = next(self.tg)
                return Farg(tmp.name)
            else:
                raise SLUCSyntaxError("ERROR: Variable {} undefined on line {} ".format(self.currtok.name, self.currtok.loc))
        else:
            if self.currtok.kind in {"int", "real"}:
                tmp = self.currtok
                self.currtok = next(self.tg)
                return Farg(tmp.name)
            if self.currtok.kind == "right-paren":
                self.currtok = next(self.tg)
                return Farg("")
        raise SLUCSyntaxError("ERROR: Invalid function argument {} on line {} ".format(self.currtok.name, self.currtok.loc))

    def term(self) -> Expr:
        """
        Term  → Fact { MulOp Fact }
        """
        left = self.fact()
        while self.currtok.kind in {"multiply", "divide", "mod"}:
            op = self.currtok.name
            self.currtok = next(self.tg)
            right = self.fact()
            left = MultExpr(left, right, op)
        return left

    def fact(self) -> Expr:
        """
        Fact  → Base {Expo Base}
        """
        left = self.base()
        while self.currtok.kind == "expo":
            self.currtok = next(self.tg)  # advance to the next token
            right = self.fact()
            left = ExpoExpr(left, right)
        return left

    def base(self) -> Expr:
        """
        Base → [UnaryOp] primary
        """
        if self.currtok.kind in {"minus", "negate"}:

            op = self.currtok.name
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryOp(tree, op)

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary  → ID | INTLIT | ( Expr ) | FuncCall
        """
        if self.currtok.kind == "ID":
            func_name=self.currtok.name
            tmp = self.currtok
            self.currtok=next(self.tg)
            if self.currtok.kind=="left-paren":
                if self.check_id_exist(func_name, self.func_id):
                    self.currtok=next(self.tg)
                    return self.funcC(tmp.name)
                else:
                    raise SLUCSyntaxError("ERROR: Function {} not defined on line {}".format(tmp.name, tmp.loc) )
            elif tmp.name in self.var_id:
                    return IDExpr(tmp.name)
            else:
                raise SLUCSyntaxError("ERROR: Variable {} undefined on line {}".format(tmp.name, tmp.loc))

        if self.currtok.kind in self.ex_dict.keys():
            tmp=self.currtok
            self.currtok=next(self.tg)
            return self.ex_dict[tmp.kind](tmp.name)


        # parse a parenthesized expression
        if self.currtok.kind == "left-paren":
            self.currtok = next(self.tg)
            tree = self.expression()
            if self.currtok.kind == "right-paren":
                self.currtok = next(self.tg)
                return tree
            else:
                # use the line number from your token object
                raise SLUCSyntaxError("ERROR: Missing right paren on line {0}".format(self.currtok.loc))
        if self.currtok.name in ["true", "false"]:
            tmp = self.currtok
            self.currtok = next(self.tg)
            return BoolExpr(tmp.name)

        # what if we get here we have a problem
        raise SLUCSyntaxError("ERROR: Unexpected token {0} on line {1}".format(self.currtok.name, self.currtok.loc))


# create our own exception by inheriting
# from Python's exception
class SLUCSyntaxError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    if len(sys.argv)>1:
        p = Parser(sys.argv[1])
    else:
        p = Parser("simple.c")
    t =p.program()
    print(t)