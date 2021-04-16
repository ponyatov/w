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
Y      += metaL.py test/metaL.py
Y      += $(shell find project -type f -regex ".+.py$$")
Y      += $(shell find user    -type f -regex ".+.py$$")
Y      += $(shell find map     -type f -regex ".+.py$$")
Y      += manage.py
E      += $(shell find src     -type f -regex ".+.erl$$")
X      += $(shell find lib     -type f -regex ".+.ex$$")
X      += $(shell find config  -type f -regex ".+.exs$$")
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
# / all

# \ django
HOST = 127.0.0.1
PORT = 12345

.PHONY: runserver
runserver: $(PY) manage.py
	$^ $@ $(HOST):$(PORT)

.PHONY: makemigrations
makemigrations: $(PY) manage.py
	$^ $@

.PHONY: migrate
migrate: $(PY) manage.py
	$^ $@

.PHONY: createsuperuser
createsuperuser: $(PY) manage.py
	$^ $@ --username dponyatov --email "dponyatov@gmail.com"

.PHONY: dumpdata
dumpdata: $(PY) manage.py
	$^ $@ --format json --indent 2 > fixture/$@.json

.PHONY: loaddata
loaddata: $(PY) manage.py
	$^ $@ fixture/user.json fixture/group.json
# / django

# \ doc
.PHONY: doc
doc:
# / doc

# \ install
.PHONY: install
install: $(OS)_install js doc
	$(MAKE) $(PIP)
	$(MAKE) createsuperuser
	$(MIX)  deps.get
	$(MAKE) rebar
	$(MAKE) update
	$(MIX)  archive.install hex phx_new 1.5.8
#	$(MIX)  ecto.create
#	$(MIX)  ecto.migrate
.PHONY: update
update: $(OS)_update
	$(PIP)   install -U    pip autopep8
	$(PIP)   install -U -r requirements.txt
	$(MAKE)  migrate
	$(REBAR) update
	$(MIX)   local.hex local.rebar
	$(MIX)   deps.get
	$(MIX)   deps.compile
	$(MIX)   deps.update --all

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
MERGE += mix.exs .formatter.exs
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
