import sys
from parser import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = Parser(sys.argv[1])
    else:
        p = Parser("simple.c")
    t = p.program()
    print(t)
    t.eval()
