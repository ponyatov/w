# \ var
MODULE  = $(notdir $(CURDIR))
OS      = $(shell uname -s)
MACHINE = $(shell uname -m)
NOW     = $(shell date +%d%m%y)
REL     = $(shell git rev-parse --short=4 HEAD)
CORES   = $(shell grep processor /proc/cpuinfo| wc -l)
# / var

# \ dir
CWD     = $(CURDIR)
BIN     = $(CWD)/bin
DOC     = $(CWD)/doc
TMP     = $(CWD)/tmp
LIB     = $(CWD)/lib
SRC     = $(CWD)/src
TEST    = $(CWD)/test
GZ      = $(HOME)/gz
# / dir

# \ tool
CURL    = curl -L -o
REBAR   = $(HOME)/bin/rebar3
ERLC    = erlc
ERL     = erl
MIX     = mix
IEX     = iex
# / tool

# \ src
# / src

# \ all
.PHONY: repl
repl:
	$(IEX)  -S mix
	$(MAKE) test
	$(MAKE) format
	$(MAKE) $@

.PHONY: test
test:
	$(MIX) test

.PHONY: format
format:
	$(MIX)  format
# / all

# \ doc
# / doc

# \ install
.PHONY: install update
install: $(OS)_install
	$(MAKE) rebar
	$(MAKE) update
update: $(OS)_update
	$(MIX)  deps.get

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# \ js
# / js
# \ erlang
.PHONY: rebar
rebar: $(REBAR)
$(REBAR):
	$(CURL) $@ https://s3.amazonaws.com/rebar3/rebar3 && chmod +x $@
	$(REBAR) local install
# / erlang
# / install
# \ merge
# / merge
