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

    # top-level function that will be called
    def program(self):
        """
            Program         →  { FunctionDef }

        """

    def block(self) -> Expr:
        if self.currtok.kind == "left-brace":
            self.currtok = next(self.tg)
            left = self.expression()
            while self.currtok.kind != "right-brace":
                self.currtok = next(self.tg)
                right = self.expression()
                left = BlockExpr(left, right)
            return left

    def assignment(self) -> Expr:
        if self.currtok.kind == "ID":
            tmp = self.currtok.name
            self.currtok = next(self.tg)
            if self.currtok.kind == "assignment":
                self.currtok = next(self.tg)
                right = self.expression()
                if self.currtok.kind == "semicolon":
                    left = AssignmentExpr(tmp, right)
                    return left
        raise SLUCSyntaxError("ERROR: Missing ; on line {}".format(self.currtok.loc))

    def ifStatement(self) -> Expr:
        if (self.currtok.kind == "Keyword") & (self.currtok.name == "if"):
            print("IfStatement")
            self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            print("left-paren")
            self.currtok = next(self.tg)
            left = self.expression()
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            right = self.statement()
            left = IfExpr(left, right)
        if (self.currtok.kind == "Keyword") & (self.currtok.name == "if"):
            print("elseStatement")
            self.currtok = next(self.tg)
            right = self.statement()
            left = IfExpr(left, right)
        return left


    def whileStatement(self) -> Expr:
        if (self.currtok.kind == "Keyword") & (self.currtok.name == "while"):
            print("whileStatement")
            self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            print("left-paren")
            self.currtok = next(self.tg)
            left = self.expression()
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            right = self.statement()
        left = WhileExpr(left, right)
        return left

    def printStmt(self) -> Expr:
        if (self.currtok.kind == "Keyword") & (self.currtok.name == "print"):
            print("printStmt")
            self.currtok = next(self.tg)
        if self.currtok.kind == "left-paren":
            print("left-paren")
            self.currtok = next(self.tg)
            left = self.printArg()
        while (self.currtok.kind == "comma"):
            self.currtok = next(self.tg)
            right = self.printArg()
            left = PrintStmtExpr(left, right)
        if self.currtok.kind == "right-paren":
            self.currtok = next(self.tg)
            left = PrintStmtExpr(left, None)
        return left

    def printArg(self)->Expr:
        ##left = self.expression()

        if self.currtok.kind == "String":  # using ID in expression
            tmp = self.currtok
            self.currtok = next(self.tg)
            return StrLitExpr(tmp.name)

        left = self.expression()
        return left

    def expression(self) -> Expr:
        left = self.conjunction()

        while self.currtok.kind == "or":
            print("expression ")
            self.currtok = next(self.tg)
            right = self.conjunction()
            left = Expr(left, right)
        return left

    def conjunction(self)->Expr:
        left = self.equality()

        while self.currtok.kind=="and":
            print("conjunction")
            self.currtok = next(self.tg)
            right = self.equality()
            left = ConjExpr(left, right)
        return left

    def equality(self):  # a == b      3*z != 99
        left = self.relation()

        while self.currtok.kind in {"equal-equal","not-equal"}:
            print("equality")
            equop=self.currtok.name
            self.currtok=next(self.tg)
            right=self.relation()
            left=EqExpr(left,right,equop)
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
            tree = self.addition()  # TODO Keeps changing!
            if self.currtok.kind == "right-paren":
                self.currtok = next(self.tg)
                return tree
            else:
                # use the line number from your token object
                raise SLUCSyntaxError("ERROR: Missing right paren on line {0}".format(self.currtok.loc))
        if self.currtok.name in ["true","false"]:
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
    t = p.whileStatement()
    print(t)
    print(t.scheme())