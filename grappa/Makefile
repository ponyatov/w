
PY = ../bin/python3

GRAMMAR = src/CoreErlang.g4
LEXER   = src/CoreErlangLexer.py

.PHONY: all
all: $(PY) src/CoreErlang.py tmp/hello.core
	$^ $@

src/CoreErlang.py: src/CoreErlangLexer.py

tmp/%.core: src/%.erl
	erlc +to_core -o tmp $<

$(LEXER): $(GRAMMAR)
	antlr4 -Dlanguage=Python3 $<

.PHONY: test format
test: all
format: all
