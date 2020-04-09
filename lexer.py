import sys
from typing import Generator, Tuple
import re




class Lexer:


    # class variables that represent a code for a "kind" of token.
    # TODO Clean this up so it is much shorter

    INTLIT = next(attr)  # 1) setattr builtin function
    PLUS = next(attr)  # 2) namedtuple
    ID = next(attr)  # 3) named tuples are not typed Typed Named Tuple in
    LPAREN = next(attr)  # the typehints doc in Python
    RPAREN = next(attr)  # 4) Class to represent a token
    EOF = next(attr)  # TODO return special end-of-file token
    MULT = next(attr)
    INT = next(attr)

    def __init__(self, fn: str):
        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

    def token_generator(self) -> Generator[Tuple[int, str], None, None]:

        token_dict = {
            ')': Lexer.RPAREN,
            '(': Lexer.LPAREN,

        }

        # TODO Can we make this more readable by putting this elsewhere?
        # check out the documentation on |
        # Don't forget about ^ and $
        # TEST TEST TEST try and break your code
        # SOLID

        digit = "[0-9_?]"

        split_patt = re.compile(
            # changes for a,b,c,d
            r"""             # Split on 
         
               (^[ \t]*".*")                              |                         #string literal   #TODO /
               (\b(?<![\._])(?<!(e[\+-])){d}+(?![\._])\b)    |   #integer
            # TODO 4e10 4e-1
               (\d(_\d|\d)*\.\d(_\d|\d)*\b|
                \b\d(_\d|\d)*(.\d(_\d|\d)*)?e[-\+]?\d(_\d|\d)*\b)  |
               
               
               
               \s     |                                 #space 
               ^[ \t]*//.*$                         |   # comments start with a //
               (bool|else |if |print| false |true |int| main| while| char| float)   | 
               (\|\|) | 
               (&&) | 
               (==) | 
               (!=) | (<) | (<=) |(>) |(>=) |(\+) |(\-) |(\*) |(\/) |(\%) |
               (\! ) |
               (\; |\, |{{ |}} |\( |\)) 
            """.format(d=digit),
            re.VERBOSE
        )

        # regular expression for an ID
        # regular expression for an integer literal

        index = 0
        for line in self.f:
            index += 1
            # save recognizing string literals and comments
            # until the end (do these last). Try and recognize
            # these *before* you split the line

            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                # TODO replace with a dictionary
                if t == '+':
                    yield (Lexer.PLUS, t, "Line {}".format(index))  # singleton
                elif t == '*':
                    yield (Lexer.MULT, t, "Line {}".format(index))
                elif t == '(':
                    yield (Lexer.LPAREN, t, "Line {}".format(index))
                elif t == ')':
                    yield (Lexer.RPAREN, t, "Line {}".format(index))
                elif type(t) == int:
                    yield (Lexer.INTLIT, t, "Line {}".format(index))
                else:
                    yield (Lexer.ID, t, "Line {}".format(index))  # singleton?


if __name__ == "__main__":

    lex = Lexer("runtest.c")  # use command line arguments

    g = lex.token_generator()

    while True:
        try:
            print(next(g))
        except StopIteration:
            print("Done")
            break