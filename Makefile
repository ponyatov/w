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
PY      = bin/python3
PIP     = bin/pip3
PEP     = bin/autopep8
PYT     = bin/pytest
REBAR   = $(HOME)/bin/rebar3
ERL     = erl
ERLC    = erlc
MIX     = mix
IEX     = iex
JAVA    = java
JAVAC   = javac
# / tool

# \ src
P      += config.py
Y      += metaL.py test_metaL.py
Y      += $(shell find project   -type f -regex ".+.py$$")
Y      += $(shell find app       -type f -regex ".+.py$$")
Y      += $(shell find user      -type f -regex ".+.py$$")
Y      += $(shell find landing   -type f -regex ".+.py$$")
Y      += $(shell find book      -type f -regex ".+.py$$")
Y      += $(shell find map       -type f -regex ".+.py$$")
Y      += $(shell find bully     -type f -regex ".+.py$$")
Y      += manage.py
E      += $(shell find src       -type f -regex ".+.erl$$")
X      += $(shell find lib       -type f -regex ".+.ex$$")
X      += $(shell find config    -type f -regex ".+.exs$$")
X      += $(shell find priv/repo -type f -regex ".+.exs$$")
X      += $(shell find priv/psql -type f -regex ".+.exs$$")
X      += .formatter.exs mix.exs
S      += $(Y) $(E) $(X)
# / src

# \ all
.PHONY: all
all: $(PY) metaL.py
	$^ $@
.PHONY: shell
shell: $(PY) metaL.py
	$^ $@
	stty echo
	$(MAKE) $@

.PHONY: repl
repl:
	$(IEX) -S mix phx.server
	$(MIX)    format
	$(MAKE)   $@
.PHONY: web
web: $(E) $(X)
	$(MIX)    phx.server

.PHONY: format
format: tmp/format_py tmp/format_ex
tmp/format_py: $(Y)
	$(PEP) --ignore=E26,E302,E401,E402,E701,E702 --in-place $? && touch $@
tmp/format_ex: $(E) $(X)
	$(MIX) format && touch $@

.PHONY: test
test: $(PYT) test_metaL.py
	$^
	$(MAKE) format

# / all

# \ eggs
.PHONY: lisp
lisp: $(PY) lis.py
	$^ $@
# / eggs

# \ django
HOST = 127.0.0.1
PORT = 12345

.PHONY: runserver
runserver: $(PY) manage.py
	$^ $@ $(HOST):$(PORT)

.PHONY: livereload
livereload: $(PY) manage.py
	$^ $@

.PHONY: makemigrations
makemigrations: $(PY) manage.py
	$^ $@
	$(MAKE) migrate

.PHONY: migrate
migrate: $(PY) manage.py
	$^ $@

.PHONY: createsuperuser
createsuperuser: $(PY) manage.py
	$^ $@ --username dponyatov --email "dponyatov@gmail.com"

.PHONY: dumpdata
dumpdata: $(PY) manage.py
	$^ $@ --format json --indent 2 > tmp/$@.json

FIXTURE = $(shell find fixture -type f -regex ".+.json$$")
.PHONY: loaddata
loaddata: $(PY) manage.py
	$^ $@ $(FIXTURE)
# / django

# \ doc
.PHONY: doc
doc: \
	doc/Erlang/LYSE_ru.pdf doc/Erlang/Armstrong_ru.pdf \
	doc/Erlang/beam-book.pdf doc/Erlang/core_erlang-1.0.3.pdf \
	doc/Erlang/FermVM.pdf \
	doc/Erlang/ElixirInAction.pdf doc/Erlang/Phoenix.pdf \
	doc/Nim/NimInAction.pdf

doc/Erlang/LYSE_ru.pdf:
	$(CURL) $@ https://github.com/mpyrozhok/learnyousomeerlang_ru/raw/master/pdf/learnyousomeerlang_ru.pdf
doc/Erlang/Armstrong_ru.pdf:
	$(CURL) $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf
doc/Erlang/ElixirInAction.pdf:
	$(CURL) $@ https://github.com/levunguyen/CGDN-Ebooks/raw/master/Java/Elixir%20in%20Action%2C%202nd%20Edition.pdf
doc/Erlang/Phoenix.pdf:
	$(CURL) $@ http://www.r-5.org/files/books/computers/languages/erlang/phoenix/Chris_McCord_Bruce_Tate_Jose_Valim-Programming_Phoenix-EN.pdf
doc/Erlang/beam-book.pdf:
	$(CURL) $@ https://github.com/happi/theBeamBook/releases/download/0.0.14/beam-book.pdf
doc/Erlang/core_erlang-1.0.3.pdf:
	$(CURL) $@ https://www.it.uu.se/research/group/hipe/cerl/doc/core_erlang-1.0.3.pdf
doc/Erlang/FermVM.pdf:
	$(CURL) $@ http://uu.diva-portal.org/smash/get/diva2:428121/FULLTEXT01.pdf

doc/Nim/NimInAction.pdf:
	$(CURL) $@ https://nim.nosdn.127.net/MTY3NjMzODI=/bmltd18wXzE1NzYxNTc0NDQwMTdfMWU4MDhiODUtZDM0Ni00OWFlLWJjYzUtMDg2ODIxMmMzMTIw

.PHONY: doxy
doxy: $(S)
	doxygen doxy.gen 1> /dev/null
# / doc

# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MAKE) createsuperuser
	$(MIX)  deps.get
	$(MAKE) rebar
	cd assets ; npm install
	$(MAKE) update
	$(MIX)  archive.install hex phx_new 1.5.8
#	$(MIX)  ecto.create
#	$(MIX)  ecto.migrate
.PHONY: update
update: $(OS)_update
	$(PIP)   install -U    pip autopep8
	$(PIP)   install -U -r requirements.txt
	$(MAKE)  migrate loaddata
	$(REBAR) update
	$(MIX)   local.hex local.rebar
	$(MIX)   deps.get
	$(MIX)   deps.compile
	$(MIX)   deps.update --all
	cd assets ; npm run deploy

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt apt.dev`

# \ py
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install -U pytest
# / py

# \ js
.PHONY: js
js:
# / js

# \ erlang
.PHONY: rebar
rebar: $(REBAR)
$(REBAR):
	$(CURL) $@ https://s3.amazonaws.com/rebar3/rebar3 && chmod +x $@
	$(REBAR) local install
	ln -fs $(HOME)/.cache/rebar3/bin/rebar3 $@
# / erlang
# / install

# \ merge
MERGE += README.md Makefile .gitignore apt.txt apt.dev LICENSE $(S)
MERGE += .vscode bin doc lib src test tmp
MERGE += requirements.txt
MERGE += mix.exs .iex.exs .formatter.exs
MERGE += gis

.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
.PHONY: shadow
shadow:
	git push -v
	git checkout $@
	git pull -v
.PHONY: release
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / merge
