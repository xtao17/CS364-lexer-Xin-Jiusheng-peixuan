from parser_sluc import *
if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = Parser(sys.argv[1])
    else:
        p = Parser("simple.c")

    try:
        t = p.program()
        t.eval()
    except SLUCSyntaxError as e:
        print(str(e))
        sys.exit()

    except SLUCTypeError as e:
        print(str(e))
        sys.exit()
