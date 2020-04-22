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

        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.currtok = next(self.tg)

    """
        Expr  →  Term { (+ | -) Term }
        Term  → Fact { (* | / | %) Fact }
        Fact  → [ - ] Primary
        Primary  → ID | INTLIT | ( Expr )
        Recursive descent parser. Each non-terminal corresponds
        to a function.
        -7  -(7 * 5)  -b   unary minus
    """

    def FunctionDef(self):
        stms = []
        decs = []
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float", "string"}:
            type = self.currtok.name

            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                id = self.currtok.name
                self.currtok = next(self.tg)
                if self.currtok.kind == "left-paren":
                    print("left-paren")
                    self.currtok = next(self.tg)
                    parm = self.params()
                    if self.currtok.kind == "right-paren":
                        print("right-paren")
                        self.currtok = next(self.tg)
                    if self.currtok.kind == "left-brace":
                        self.currtok = next(self.tg)
                        while(self.currtok.name not in {"int", "bool", "float", "string"}):
                            decs.append(self.declaration())
                            self.currtok=next(self.tg)
                            stms.append(self.statement())
                            self.currtok=next(self.tg)

                        if self.currtok.kind == "right-brace":
                            return FunctionDefExpr(self, type, id, parm, decs, stms)
        raise SLUCSyntaxError("ERROR: Invalid function definition on line {}".format(self.currtok))
    # top-level function that will be called
    def program(self):
        """
            Program         →  { FunctionDef }
        """

    def params(self) -> Expr:
        args =[]
        if self.currtok.kind == "Keyword" and self.currtok.name in{"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                right = self.primary()
            else:
                raise SLUCSyntaxError("ERROR: Invalid param on line {}".format(self.currtok.loc))

            while (self.currtok.kind == "comma"):
                self.currtok = next(self.tg)
                args.append(self.currtok.name)
                self.currtok = next(self.tg)
                args.append(self.primary())

            return ParamExpr(left, right, args)

    def declaration(self) -> Expr:
        if self.currtok.kind == "Keyword" and self.currtok.name in {"int", "bool", "float"}:
            left = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "ID":
                right = self.currtok.name
                self.currtok = next(self.tg)
                return DecExpr(left, right)
        raise SLUCSyntaxError("ERROR: Invalid declaration on line {}".format(self.currtok))


    def statement(self) -> Expr:
        if self.currtok.kind == "semicolon":  # using ID in expression
            tmp = self.currtok
            self.currtok = next(self.tg)
            return StmtExpr(tmp.name)
        if self.currtok.kind == "left-brace":
            return self.block()
        if self.currtok.kind == "Keyword" and self.currtok.name == "if":
            return self.ifstatement()
        if self.currtok.kind == "Keyword" and self.currtok.name == "while":
            return self.whilestatement()
        if self.currtok.kind == "Keyword" and self.currtok.name == "print":
            return self.printstmt()
        if self.currtok.kind == "Keyword" and self.currtok.name == "return":
            return self.returnstmt()
        if self.currtok.kind == "ID":
            return self.assignment()

    def returnstmt(self) -> Expr:
        if self.currtok.kind == "Keyword" and self.currtok.name == "return":
            self.currtok = next(self.tg)
            expr = self.expression()
            if self.currtok.kind == "semicolon":
                print("returnstmt")
                self.currtok = next(self.tg)
                return ReturnExpr(expr)
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(self.currtok.loc))

    def block(self) -> Expr:
        stmts = []
        if self.currtok.kind == "left-brace":
            self.currtok = next(self.tg)
            stmt = self.statement()
            while self.currtok.kind != "right-brace":
                stmts.append(self.statement())
            self.currtok = next(self.tg)
            return BlockExpr(stmt, stmts)

    def assignment(self) -> Expr:
        if self.currtok.kind == "ID":
            id = self.primary()
            if self.currtok.kind == "assignment":
                self.currtok = next(self.tg)
                expr = self.expression()
                if self.currtok.kind == "semicolon":
                    print("assigment")
                    self.currtok = next(self.tg)
                    assign = AssignmentExpr(id, expr)
                    return assign
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(self.currtok.loc))

    def ifstatement(self) -> Expr:
        if self.currtok.kind == "Keyword" and self.currtok.name == "if":
            print("ifstatement")
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

    def whilestatement(self) -> Expr:
        if self.currtok.kind == "Keyword" and self.currtok.name == "while":
            print("whileStatement")
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

    def printstmt(self) -> Expr:
        prtargs = []
        left = Expr(None, None)
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

        while self.currtok.kind in {"multiply", "divide"}:
            self.currtok = next(self.tg)
            right = self.fact()
            left = MultExpr(left, right)

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

        # parse a real literal
        if self.currtok.kind == "real":
            print("floatlit")
            tmp = self.currtok
            self.currtok = next(self.tg)
            return FloatLitExpr(tmp.name)

        # parse an ID
        if self.currtok.kind == "ID":  # using ID in expression
            print("id")
            tmp = self.currtok
            self.currtok = next(self.tg)
            return IDExpr(tmp.name)

        # parse an integer literal
        if self.currtok.kind == "int":
            print("intlit")
            tmp = self.currtok
            self.currtok = next(self.tg)
            return IntLitExpr(tmp.name)

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
            return Expr(tmp.name)

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
    t = p.params()
    print(t)