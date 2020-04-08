import sys
from typing import Generator, Tuple
import re
class Lexer:

    # class variables that represent a code for a "kind" of token.
    # TODO Clean this up so it is much shorter
    INTLIT = 0        # 1) setattr builtin function
    PLUS   = 1        # 2) namedtuple
    ID     = 2        # 3) named tuples are not typed Typed Named Tuple in
    LPAREN = 3        #     the typehints doc in Python
    RPAREN = 4        # 4) Class to represent a token
    EOF    = 5 # TODO return special end-of-file token
    MULT   = 6

    def __init__(self, fn: str):
        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

    def token_generator(self) -> Generator[Tuple[int, str], None, None]:

        # TODO Can we make this more readable by putting this elsewhere?
        # check out the documentation on |
        # Don't forget about ^ and $
        # TEST TEST TEST try and break your code
        # SOLID
        split_patt = re.compile(
            # changes for a,b,c,d
            r"""             # Split on 
               ^(\d+)$    |                            #integer
               ((\d+)(\.[0-9]+)?)(e(\+|-)?(\d+))?    |   # real number(scientific notation)
               #TODO real include integer?? +,- sign before??
               
               ([0-9]+.*_*[0-9]+)    |   # integers and floats with underscores  TODO - check 1._23
               ([_a-zA-Z][_\w]*) | # ID
               ("[\w\s]*"$)  |   # TODO - check \"
               (//\w*)     # comments start with a //
            """,
            re.VERBOSE
        )

        # regular expression for an ID
        # regular expression for an integer literal

        for line in self.f:

            # save recognizing string literals and comments
            # until the end (do these last). Try and recognize
            # these *before* you split the line

            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                # TODO replace with a dictionary
                if t == '+':
                    yield (Lexer.PLUS, t)   # singleton
                elif t == '*':
                    yield (Lexer.MULT, t)
                elif t == '(':
                    yield (Lexer.LPAREN, t)
                elif t == ')':
                    yield (Lexer.RPAREN, t)
                else:
                    yield (Lexer.ID, t)    # singleton?


if __name__ == "__main__":

    lex = Lexer("test.txt")  # use command line arguments

    g = lex.token_generator()

    while True:
        try:
            print(next(g))
        except StopIteration:
            print("Done")
            break
