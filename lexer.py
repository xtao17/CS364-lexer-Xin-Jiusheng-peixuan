import sys
from typing import Generator, Tuple
import re


def find_matches(d, item):
    for k in d:
        if re.fullmatch(k, item):
            return d[k]


class Lexer:


    # class variables that represent a code for a "kind" of token.



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
        real = "(\d(_\d|\d)*\.\d(_\d|\d)*|\d(_\d|\d)*(.\d(_\d|\d)*)?e[-\+]?\d(_\d|\d)*)"
        integer = "\d+[\d_]*\d+|\d+"

        keyword = "(bool)|(else)|(if)|(print)|(false)|(true)|(int)|(main)|(while)|(char)|(float)"
        string = '^[ \t]*".*"'
        illegrealToken = ""

        # Operators || && == != < <= > >= + - * / % !
        plus = "(?<!e)\+"
        minus = "(?<!e)-"
        Or = "(\|\|)"
        And = "&&"
        equi = "(==)"
        neq = "(!=)"
        les = "(<)"
        leq = "(<=)"
        gre = "(>)"
        geq = "(>=)"
        ass = "(=)"
        semico = ";"
        comma = ","
        lbrace = "\{"
        rbrace = "\}"
        lparen = "\("
        rparen = "\)"
        lbracket = "\["
        rbracket = "\]"
        mod = "%"
        negate = "!"
        mul = "\*"
        div = "\/"
        arrayAccess = "\[\]"



        id = "[_a-zA-Z][_a-zA-Z0-9]*"
        # 3. .4 .4 3.3.3 4ee5 e4e5 4.e5 1._e
        illegreal="(\d)*.$|^.(\d)*"
        token_dict = {

            integer: "int",
            real: "real",
            string: "String",
            keyword: "Keyword",
            plus: "plus",
            minus: "minus",
            Or: "or",
            And: "and",
            equi: "equal-equal",
            neq: "not-equal",
            les: "less-than",
            leq: "less-equal",
            gre: "greater-than",
            geq: "greater-equal",
            ass: "assignment",
            semico: "semicolon",
            comma: "comma",
            lbrace: "left-brace",
            rbrace: "right-brace",
            lparen: "left-paren",
            rparen: "right-paren",
            lbracket: "left-bracket",
            rbracket: "right-bracket",
            id: "ID",
            mod: "mod",
            negate: "negate",
            mul: "multiply",
            div: "divide",
            arrayAccess:"arrayAccess"

        }
        error_message_dict={
            illegreal: "illegal-realnumber"

        }

        split_patt = re.compile(
            # changes for a,b,c,d
            r"""             # Split on 
              (\"([^\\\"]|\\.)*\")|   #string
              \s           |                                 #space 
               [ \t]*//.*$ |   # comments start with a //
               #operators
               (\|\|)       | 
               (&&)         | 
               (==)         |  
               (!=) | (<) | (<=) |(>) |(>=) |(=)|
               ((?<!e)\+)   |
               ((?<!e)-)    |
               (\*) |(\/) |(\%) |
               (\! ) |
               #puncuation
               (\; |\, |\{ |\} |\( |\)) 
            """,
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
                if (find_matches(token_dict, t) == None):
                    yield (find_matches(error_message_dict, t),t, "Line {}".format(index))

                else:
                    yield (find_matches(token_dict, t), t, "Line {}".format(index))



if __name__ == "__main__":

    lex = Lexer("test.sluc")  # use command line arguments

    g = lex.token_generator()

    while True:
        try:
            print(next(g))
        except StopIteration:
            print("Done")
            break