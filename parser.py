from lexer import Lexer
from ast import *
import sys
"""
  Program         →  { FunctionDef }
  FunctionDef     →  Type id ( Params ) { Declarations Statements }
  Params          →  Type id { , Type id } | ε
  Declarations    →  { Declaration }
  Declaration     →  Type  id  ;
  Type            →  int | bool | float
  Statements      →  { Statement }
  Statement       →  ; | Block | Assignment | IfStatement |
                     WhileStatement |  PrintStmt | ReturnStmt
  ReturnStmt      →  return Expression ;
  Block           →  { Statements }
  Assignment      →  id = Expression ;
  IfStatement     →  if ( Expression ) Statement [ else Statement ]
  WhileStatement  →  while ( Expression ) Statement
  PrintStmt       →  print(PrintArg { , PrintArg })
  PrintArg        →  Expression | stringlit
  Expression      →  Conjunction { || Conjunction }
  Conjunction     →  Equality { && Equality }
  Equality        →  Relation [ EquOp Relation ]
  Relation        →  Addition [ RelOp Addition ]
  Addition        →  Term { AddOp Term }
  Term            →  Factor { MulOp Factor }
  Factor          →  [ UnaryOp ] Primary
  UnaryOp         →  - | !
  Primary         →  id | intlit | floatlit | ( Expression )
  RelOp           →  < | <= | > | >=   AddOp           →  + | -  MulOp           →  * | / | %  EquOp           →  == | !=
"""


class Parser:
    def __init__(self, fn: str):
        self.var_id=[]
        self.func_id=[]
        self.level = 0
        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.currtok = next(self.tg)
        self.ex_dict={
            "real":(lambda x:FloatLitExpr(x)),
            "int":(lambda x:IntLitExpr(x))
        }
        self.stmt_dict = {
            "if":(lambda x: self.ifstatement()),
            "while":(lambda x: self.whilestatement()),
            "print":(lambda x: self.printstmt()),
            "return":(lambda x:self.returnstmt()),
            "ID":(lambda x:self.assignment())
         }

    def formctrl(self) -> str:
        return "\t"*self.level

    def check_id_exist(self,var_name,id_list,type):
        if var_name not in id_list:
            if type=="v":
                raise SLUCSyntaxError("ERROR: variable {} undefined".format(var_name))
            if type=="f":
                raise SLUCSyntaxError("ERROR: function {} undefined".format(var_name))

    def program(self) -> Program:
        funcdefs =[]
        while self.currtok != None and self.currtok.name != "EOF":
            funcdefs.append(self.functiondef())

        return Program(funcdefs)

    def functiondef(self) -> FunctionDef:
        stms = []
        decs = []
        currentline = self.currtok.loc
        self.level = 0
        self.var_id.clear()
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            type = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID" or (self.currtok.kind=="Keyword" and self.currtok.name=="main"):
                self.func_id.append(self.currtok.name)
                id=IDExpr(self.currtok.name)
                # add id to parameter list
                self.currtok = next(self.tg)
                if self.currtok.kind == "left-paren":
                    self.currtok = next(self.tg)
                    parm = self.params()
                    if self.currtok.kind == "right-paren":
                        self.currtok = next(self.tg)
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
                self.var_id.append(self.currtok.name)
                right = IDExpr(self.currtok.name)
                self.currtok = next(self.tg)
            else:
                raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok))
            if self.currtok.kind=="semicolon":
                self.currtok = next(self.tg)
                return Declaration(left, right, self.formctrl())
        raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok))


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
        self.check_id_exist(self.currtok.name,self.var_id,"v")
        id = IDExpr(self.currtok.name)

        self.currtok = next(self.tg)
        if self.currtok.kind == "assignment":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "semicolon":
                self.currtok = next(self.tg)
                assign = AssignmentStatement(id, expr, self.formctrl())
                return assign
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(currentline))

    def ifstatement(self) -> Statement:
        self.level += 1
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
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
            self.currtok = next(self.tg)  # advance to the next token
            # because we matched a +
            right = self.term()
            left = AddExpr(left, right)

        return left

    def term(self) -> Expr:
        """
        Term  → Exp { MulOp Exp }
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
        Fact  → [ - ] Primary
            e.g., -a  -(b+c)  -6    (b+c) a 6
        """
        left = self.base()

        while self.currtok.kind == "expo":
            self.currtok = next(self.tg)  # advance to the next token

            right = self.fact()
            left = ExpoExpr(left, right)

        return left

    def base(self) -> Expr:
        if self.currtok.kind == "minus":
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryMinus(tree)

        if self.currtok.kind == "negate":
           self.currtok = next(self.tg)
           tree = self.primary()
           return UnaryNegate(tree)

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary  → ID | INTLIT | ( Expr ) | FuncCall
        """
        arguments=[]
        if self.currtok.kind == "ID":
            func_name=self.currtok.name
            tmp = self.currtok
            self.currtok=next(self.tg)
            if self.currtok.kind=="left-paren":
                self.check_id_exist(func_name, self.func_id,"f")
                self.currtok=next(self.tg)
                while(self.currtok.kind!="right-paren"):
                    arguments.append(self.expression())
                self.currtok = next(self.tg)

                return FuncCExpr(func_name,arguments)
            else:
                 return IDExpr(tmp.name)

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
    p = Parser('simple.c')
    t =p.program()
    print(t)