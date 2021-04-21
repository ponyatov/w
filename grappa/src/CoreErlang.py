# https://github.com/antlr/antlr4/blob/master/doc/python-target.md

import os,sys,re

from CoreErlangLexer import *
from CoreErlangParser import *

if __name__ == '__main__':
    corefile = sys.argv[1]
    assert re.match(r'.+\.core$',corefile)
    source = FileStream(corefile)
    lexer = CoreErlangLexer(source)
    tokens = CommonTokenStream(lexer)
    parser = CoreErlangParser(tokens)
    print(parser.module())
