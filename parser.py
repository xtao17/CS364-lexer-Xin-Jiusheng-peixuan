from lexer import Lexer, Token
from ast import *

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



    def check_id_exist(self,var_name,id_list):
        if var_name not in id_list:
            var_id=[]
            for element in self.var_id:
                var_id.append(element[0])
            if id_list==var_id:
                raise SLUCSyntaxError("ERROR: variable {} undefine".format(var_name))
            func_id=[]
            for element in self.func_id:
                func_id.append(element[0])
            if id_list==func_id:
                raise SLUCSyntaxError("ERROR: function {} undefine".format(var_name))
    def program(self) -> Program:

        funcdefs =[]
        while self.currtok != None and self.currtok.name != "EOF":
            funcdefs.append(self.functiondef())

        return Program(funcdefs)

    def functiondef(self) -> FunctionDef:
        stms = []
        decs = []
        self.var_id.clear()
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            type = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                self.func_id.append([self.currtok.name,type])
                id=IDExpr(self.currtok.name)
                # add id to parameter list
                self.currtok = next(self.tg)
                if self.currtok.kind == "left-paren":
                    print("left-paren")
                    self.currtok = next(self.tg)
                    parm = self.params()
                    if self.currtok.kind == "right-paren":
                        print("right-paren")
                        self.currtok = next(self.tg)
                    if self.currtok.kind == "left-brace":
                        print("leftbrace")
                        self.currtok = next(self.tg)
                        while(self.currtok.name in {"int", "bool", "float"}):
                            print("dec")
                            print(self.currtok.name)

                            decs.append(self.declaration())
                            print(self.currtok.name)
                        while(self.currtok.kind != "right-brace"):
                            stms.append(self.statement())
                            if self.currtok.name in  {"int", "bool", "float"}:
                                raise SLUCSyntaxError("ERROR: declarations must be written before statements on line {}".format(self.currtok.loc))

                        self.currtok = next(self.tg)
                        return FunctionDef(type, id, parm, decs, stms)

        raise SLUCSyntaxError("ERROR: Invalid function definition on line {}".format(self.currtok.loc))

    def params(self) -> Expr:
        args =[]
        if self.currtok.kind == "Keyword" and self.currtok.name in{"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                self.var_id.append([self.currtok.name,left])
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
                self.var_id.append([self.currtok.name,type])
                self.currtok = next(self.tg)
            return ParamExpr(left, right, args)

        elif self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            return ParamExpr(None, None)

        raise SLUCSyntaxError("ERROR: Invalid param on line {}".format(self.currtok.loc))

    def declaration(self) -> Expr:
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                #  add id
                self.var_id.append(self.currtok.name)
                right = IDExpr(self.currtok.name)
                self.currtok = next(self.tg)
            if self.currtok.kind=="semicolon":
                self.currtok = next(self.tg)
                return DecExpr(left, right)
        raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok))


    def statement(self) -> Expr:
        if self.currtok.kind == "semicolon":  # using ID in expression
            tmp = self.currtok
            self.currtok = next(self.tg)
            return StmtExpr(tmp.name)
        if self.currtok.kind == "left-brace":
            print(self.currtok.name)
            return self.block()

        if self.currtok.kind == "Keyword":
            item=self.stmt_dict[self.currtok.name](self)
            return item

        if self.currtok.kind == "ID":
            item=self.stmt_dict[self.currtok.kind](self)
            return item

        raise SLUCSyntaxError("ERROR: Invalid statement {} on line {}".format(self.currtok.name, self.currtok.loc))

    def returnstmt(self) -> Expr:
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        expr = self.expression()
        if self.currtok.kind == "semicolon":
            print("returnstmt")
            self.currtok = next(self.tg)
            return ReturnExpr(expr)
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(currentline))

    def block(self) -> Expr:
        stmts = []
        self.currtok = next(self.tg)
        stmt = self.statement()
        while self.currtok.kind != "right-brace":
            stmts.append(self.statement())
        self.currtok = next(self.tg)
        return BlockExpr(stmt, stmts)

    def assignment(self) -> Expr:
        currentline = self.currtok.loc
        self.check_id_exist(self.currtok.name,self.var_id)
        id = IDExpr(self.currtok.name)
        self.currtok = next(self.tg)
        if self.currtok.kind == "assignment":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "semicolon":
                print("assigment")
                self.currtok = next(self.tg)
                assign = AssignmentExpr(id, expr)
                return assign
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(currentline))

    def ifstatement(self) -> Expr:
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            print("left-paren")
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "right-paren":
                print("right-paren")
                self.currtok = next(self.tg)
                stmt = self.statement()

                if self.currtok.kind == "Keyword" and self.currtok.name == "else":
                    print("elseStatement")
                    self.currtok = next(self.tg)
                    elsestmt = self.statement()
                    return IfExpr(expr, stmt, elsestmt)

                return IfExpr(expr, stmt)

        raise SLUCSyntaxError("ERROR: Invalid ifstatement on line {}".format(currentline))

    def whilestatement(self) -> Expr:
        currentline = self.currtok.loc
        self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            print("left-paren")
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "right-paren":
                print("right-paren")
                self.currtok = next(self.tg)
                stmt = self.statement()
                return WhileExpr(expr, stmt)
        raise SLUCSyntaxError("ERROR: Invalid whilestatement on line {}".format(currentline))

    def printstmt(self) -> Expr:
        currentline = self.currtok.loc
        prtargs = []

        if self.currtok.kind == "Keyword" and self.currtok.name == "print":
            print("printStmt")
            self.currtok = next(self.tg)
            if self.currtok.kind == "left-paren":
                print("left-paren")
                self.currtok = next(self.tg)
                prtarg = self.printarg()
        while (self.currtok.kind == "comma"):
            self.currtok = next(self.tg)
            prtargs.append(self.printarg())
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            left = PrintStmtExpr(prtarg, prtargs)
            return left
        raise SLUCSyntaxError("ERROR: Invalid print statement on line {}".format(currentline))

    def printarg(self) -> Expr:
        if self.currtok.kind == "String":
            print("string")
            tmp = self.currtok
            self.currtok = next(self.tg)
            return StrLitExpr(tmp.name)
        print("printExpr")
        return StrLitExpr(self.expression())

    def expression(self) -> Expr:
        left = self.conjunction()
        while self.currtok.kind == "or":
            print("expression ")
            self.currtok = next(self.tg)
            right = self.conjunction()
            left = Expr(left, right)
        return left

    def conjunction(self) -> Expr:
        left = self.equality()

        while self.currtok.kind == "and":
            print("conjunction")
            self.currtok = next(self.tg)
            right = self.equality()
            left = ConjExpr(left, right)
        return left

    def equality(self):  # a == b      3*z != 99
        left = self.relation()

        if self.currtok.kind in {"equal-equal", "not-equal"}:
            print("equality")
            equop = self.currtok.name
            self.currtok = next(self.tg)
            right = self.relation()
            left = EqExpr(left, right, equop)
        return left

    def relation(self) -> Expr:  # a < b
        left = self.addition()
        while self.currtok.kind in {"less-than", "less-equal", "greater-than", "greater-equal"}:
            print("relation")
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
        Term  → Fact { * Fact }
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

        # only advance to the next token on a successful match.
        if self.currtok.kind == "minus":
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryMinus(tree)

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary  → ID | INTLIT | ( Expr )
        """
        arguments=[]
        if self.currtok.kind == "ID":
            func_name=self.currtok.name
            tmp = self.currtok
            self.currtok=next(self.tg)
            if self.currtok.kind=="left-paren":
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
            print("expr")
            tree = self.expression()  # TODO Keeps changing!
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
    t = p.program()
    print(t)
