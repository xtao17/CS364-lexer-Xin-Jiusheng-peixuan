'''
Lexer Project
Peixuan,Xin,Jiusheng
'''
import sys
from typing import Generator, Tuple
import re


class Token:
    '''
    this class includes all kind of tokens
    '''

    # define the possible tokens

    real = "(\d(_\d|\d)*\.\d(_\d|\d)*|\d(_\d|\d)*(.\d(_\d|\d)*)?e[-\+]?\d(_\d|\d)*)"
    integer = "\d+[\d_]*\d+|\d+"
    keyword = "(bool)|(else)|(if)|(print)|(false)|(true)|(int)|(main)|(while)|(char)|(float)|(return)"
    string = '".*"'
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
    expo = "\*\*"
    negate = "!"
    mul = "\*"
    div = "\/"
    arrayAccess = "\[\]"
    leftShift = "<<"
    rightShift = ">>"
    id = "[_a-zA-Z][_a-zA-Z0-9]*"
    # label the tokens
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
        arrayAccess: "arrayAccess",
        leftShift: "shift left",
        rightShift: "shift right",
        expo : "expo"
    }
    '''
    constructor take the token and the location
    precondition for t: t must be a string
    precondition for loc: loc must be a integer
    '''
    def __init__(self, t:str, loc:int):
        if self.find_matches(Token.token_dict, t):
            self.kind = self.find_matches(Token.token_dict, t)
        else:
            self.kind = "illegal token"
        self.name = t
        self.loc = loc


    '''
    match the kind of token in the dictionary
    d represents a dictionary
    '''
    def find_matches(self, d, item):
        for k in d:
            if re.fullmatch(k, item):
                return d[k]


class Lexer:
    """
    Lexer class to reads a file, splits and generates tokens
    """

    #  constructor that takes a file name and split them into tokens
    def __init__(self, fn: str):
        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

    # method for generate tokens
    def token_generator(self) -> Generator[Tuple[str, str, int], None, None]:
        split_patt = re.compile(
            r"""             # Split on 
              ("(?:[^\\\"]|\\.)*")|   #string
              \s           |          #space 
               [ \t]*//.*$ |          # comments start with a //
               (\|\|)       |         # and operators
               (&&)         | 
               (==)         |  
               (!=) | ((?<!<)<(?![<=]))  | (<=) |((?<!>)>(?![>=]))  |   (<<)    |
               (>>)|(>=) |(=)|
               ((?<!e)\+)   |
               ((?<!e)-)    |
               (\*?\*) |(\/) |(\%) |
               (\! ) |
               (\; |\, |\{ |\} |\( |\)) # punctuation
            """,
            re.VERBOSE
        )

        index = 0  # line number
        for line in self.f:
            index += 1
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                yield Token(t, index)

        yield Token("EOF", -1)


if __name__ == "__main__":

    lex = Lexer("lexertest.c")
    g = lex.token_generator()

    # formatted print the token table
    print("%-30s %-70s %s" % ("Token", "Name", "Line Number"))
    print("----------------------------------------------------------------------------------------------------------------")
    while True:
        try:
            temp = next(g)
            print("%-30s %-70s %s" % (temp.kind, temp.name, temp.loc))

        except StopIteration:
            print("Done")
            break