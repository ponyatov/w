import config

import os, sys, re
import datetime as dt

MODULE = sys.argv[0].split('/')[-1].split('.')[0]


## base object graph node = frame
class Object:
    def __init__(self, V):
        assert not isinstance(V, Object)
        ## type/class tag /required for PLY/
        self.type = self.__class__.__name__.lower()
        ## scalar value: name, number, string,..
        self.value = V
        ## associative array = namespace = map
        self.slot = {}
        ## ordered container = vector = stack = queue = AST
        self.nest = []
        ## global unical id
        self.gid = id(self)

    def box(self, that):
        if isinstance(that, Object): return that
        if isinstance(that, str): return S(that)
        raise TypeError(['box', type(that), that])

    ## @name dump

    def __repr__(self): return self.dump(test=False)
    def test(self): return self.dump(test=True)

    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # head
        ret = self.pad(depth) + self.head(prefix, test)
        # cycle
        if not depth: cycle = []
        if self.gid in cycle: return ret + ' _/'
        else: cycle.append(self.gid)
        # clot{}
        for i in self.keys():
            ret += self[i].dump(cycle, depth + 1, f'{i} = ', test)
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j}: ', test)
        # subtree
        return ret

    def pad(self, depth): return '\n' + '\t' * depth

    def head(self, prefix='', test=False):
        gid = f' {self.gid:x}' if not test else ''
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    def tag(self): return self.type
    def val(self): return f'{self.value}'

    def __format__(self, spec):
        return self.head()

    ## @name operator

    def keys(self): return sorted(self.slot.keys())

    def __getitem__(self, key):
        if isinstance(key, str): return self.slot[key]
        if isinstance(key, int): return self.nest[key]
        raise TypeError([f'A[key:{key.__class__.__name__}]=B', key, self])

    def __setitem__(self, key, that):
        that = self.box(that)
        if isinstance(key, str): self.slot[key] = that; return self
        if isinstance(key, int): self.nest[key] = that; return self
        raise TypeError([f'A[key:{key.__class__.__name__}]=B', key, self])

    def __lshift__(self, that):
        that = self.box(that)
        return self.__setitem__(that.tag(), that)

    def __rshift__(self, that):
        that = self.box(that)
        return self.__setitem__(that.val(), that)

    def __floordiv__(self, that):
        that = self.box(that)
        self.nest.append(that); return self

    ## @name stack operations

    def drop(self): self.nest.pop(); return self

    ## @name computation

    def eval(self, env):
        raise NotImplementedError('eval', self)

    def apply(self, env, that):
        raise NotImplementedError('apply', self, that)


class Primitive(Object):
    def eval(self, env): return self
    ## source code generation

    def gen(self, depth=0, to=None):
        return f'{to.tab*depth}{self.value}'

## a.k.a. atom, keyword, symbol
class Name(Primitive):
    def eval(self, env):
        return env[self.value]

class String(Primitive): pass

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

## machine hexadecimal number
class Hex(Integer): pass

## binary string
class Bin(Integer): pass


class Container(Object): pass

class Map(Container): pass


class IO(Object): pass

class Time(IO): pass

class Path(IO): pass


class Dir(IO):
    def __init__(self, V):
        super().__init__(V)
        self.path = Path(self.value)

    def sync(self):
        try: os.mkdir(self.path.value)
        except FileExistsError: pass
        for j in self.nest: j.sync()

    def __floordiv__(self, that):
        if isinstance(that, Dir) or isinstance(that, File):
            super().__floordiv__(that)
            that.path.value = f"{self.path.value}/{that.path.value}"
            print(that, that.path)
            return self
        raise TypeError(['//', type(that), that])


class File(IO):
    def __init__(self, V, ext='', tab=' ' * 4, comment='#', commend=None):
        super().__init__(V + ext)
        self.path = Path(self.value)
        self.tab = tab
        ## line comment / start block comment
        self.comment = comment
        ## end block comment
        self.commend = commend
        ## file header
        self.top = Sec('top')
        ## file footer
        self.bot = Sec('bot')

    def sync(self):
        with open(self.path.value, 'w') as F:
            for i in self.top: F.write(i.gen(to=self))
            for j in self.nest: F.write(j.gen(to=self))
            for k in self.bot: F.write(k.gen(to=self))

## special console singleton for file-based output (code generation)
class Console(File):
    tab = '\t'

    def __init__(self, V=''):
        super().__init__(V)
        self.tab = '\t'


## EDS: Executable Data Structure (c)
class Active(Object): pass

## function
class Fn(Active): pass

## operator
class Op(Active): pass
class Tick(Op):
    def eval(self, env):
        assert len(self.nest) == 1
        return self.nest[0]

## namespace = environment
class Env(Active, Map): pass


glob = Env('global'); glob << glob >> glob


class Meta(Object): pass

## source code block
class S(Meta):
    def __init__(self, start=None, end=None, pfx=None):
        super().__init__(start)
        self.start = start
        self.end = end
        self.pfx = pfx

    ## source code generation
    def gen(self, depth=0, to=Console):
        ret = ''
        if self.pfx != None:
            ret += f'{to.tab*depth}{self.pfx}\n' if self.pfx else '\n'
        if self.start != None:
            ret += f'{to.tab*depth}{self.start}\n' if self.start else '\n'
        for j in self.nest:
            ret += j.gen(depth + 1, to)
        if self.end != None:
            ret += f'{to.tab*depth}{self.end}\n'
        return ret

## source section
class Sec(Meta):
    ## source code generation
    def gen(self, depth=0, to=Console):
        ret = f'{to.tab*depth}{to.comment} \\ {self.value}\n'
        for j in self.nest:
            ret += j.gen(depth + 0, to)
        ret += f'{to.tab*depth}{to.comment} / {self.value}\n'
        return ret

class Module(Meta):
    def __format__(self, spec=None):
        if not spec:
            return f'{self.value}'
        if spec == 'm':
            return f'{self.value.capitalize()}'
        if spec == 'l':
            return f'{self.value.lower()}'
        if spec == 'u':
            return f'{self.value.upper()}'
        raise TypeError(['__format__', spec, self])

class Class(Meta):
    def __init__(self, C):
        super().__init__(C.__name__)
        self.clazz = C

    def apply(self, env, that):
        assert isinstance(that, Object)
        print(self.clazz)
        return self.clazz(that)

class Method(Meta, Fn): pass


class Net(IO): pass

class Socket(Net): pass

class IP(Net): pass

class Port(Net): pass


class Web(Net): pass

class Engine(Web):
    def __init__(self, V='Flask'): super().__init__(V)


## HTML blocked
class HTML(Web): pass

## HTML inline
class HTMLI(Web): pass


## VSCode hints
class VSCode(Object): pass

## `.vscode/tasks.json`
class Task(VSCode):
    def __init__(self, that):
        assert isinstance(that, Object)
        super().__init__(that.value)

    def eval(self, env):
        return (S('{', '}')
                // f'"label":          "make: {self.value}",'
                // f'"type":           "shell",'
                // f'"command":        "make {self.value}",'
                // f'"problemMatcher": []'
                ).gen()

    def apply(self, env, that):
        assert isinstance(that, Object)
        return self
# Task `install


glob >> Class(Task)

######################################################################### lexer

import ply.lex as lex

tokens = ['q', 'integer', 'name', 'tick']

t_ignore = ' \t\r'
t_ignore_comment = r'\#.*'

def t_nl(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_q(t):
    r'\?'
    return t

def t_integer(t):
    r'[+\-]?[0-9]+'
    t.value = Integer(t.value); return t

def t_tick(t):
    r'`'
    t.value = Tick(t.value); return t

def t_name(t):
    r'[^ \t\r\n\#]+'
    t.value = Name(t.value); return t

def t_error(t): raise SyntaxError(t)


lexer = lex.lex()

######################################################################## parser

import ply.yacc as yacc

def p_REPL_none(p):
    ' REPL : '
    pass
def p_REPL_glob(p):
    ' REPL : REPL q '
    print(glob)
def p_REPL_recur(p):
    ' REPL : REPL ex '
    ret = p[2].eval(glob)
    print(ret)

def p_ex_apply(p):
    ' ex : apply '
    p[0] = p[1]
def p_apply(p):
    ' apply : ex ex '
    a = p[1].eval(glob)
    b = p[2].eval(glob)
    p[0] = a.apply(glob, b)

def p_ex_integer(p):
    ' ex : integer '
    p[0] = p[1]
def p_ex_name(p):
    ' ex : name '
    p[0] = p[1]

def p_ex_quote(p):
    ' ex : tick ex '
    p[0] = p[1] // p[2]

def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)


########################################################## readline.lib tunings

import readline, atexit

history = os.path.join(os.path.abspath('.'), 'tmp', '.metaL.history')

atexit.register(lambda:
                readline.write_history_file(history))
if os.path.exists(history):
    readline.read_history_file(history)

def completer():
    def metaL_complete(text, state):
        words = [i for i in glob.keys() if i.startswith(text)] + [None]
        return words[state]
    return metaL_complete


readline.set_completer(completer())

def complete_match(substitution, matches, longest_match_length):
    print(glob)
    print('substitution', substitution)
    print('mathes', matches)
    print('longest_match_length', longest_match_length)
    print('\t'.join(map(lambda i: glob[i].head(
        prefix=f'{i} ', test=True), matches)))


readline.set_completion_display_matches_hook(complete_match)

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


################################################## source code watcher restarts

import signal

def shell():
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class event_handler(FileSystemEventHandler):
        def on_closed(self, event):
            if not event.is_directory:
                # sio.emit('reload', f'{event}')
                os.kill(os.getpid(), signal.SIGWINCH) # todo: terminal freeze
                readline.write_history_file(history)
                os._exit(0)
    watch = Observer()
    watch.schedule(event_handler(), sys.argv[0])
    watch.schedule(event_handler(), 'metaL.py')
    # watch.schedule(event_handler(), 'static', recursive=True)
    # watch.schedule(event_handler(), 'templates', recursive=True)
    watch.start()


########################################################## Read-Eval-Print-Loop

import traceback

def REPL():
    while True:
        try:
            parser.parse(input('\nmetaL> ').strip())
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exc()
            print(f'{type(e).__name__} {__file__}:{e.__traceback__.tb_lineno}\n\t{e}')


#################################################### generative metaprogramming

class gitiFile(File):
    def __init__(self, V='', ext='.gitignore', comment='#'):
        super().__init__(V, ext, comment=comment)
        self.bot // '!.gitignore'

class Makefile(File):
    def __init__(self, V='Makefile', tab='\t', ext='', comment='#'):
        super().__init__(V, ext, tab=tab, comment=comment)

class jsonFile(File):
    def __init__(self, V, ext='.json', comment='//'):
        super().__init__(V, ext, comment=comment)

class mdFile(File):
    def __init__(self, V, ext='.md', comment='//'):
        super().__init__(V, ext, comment=comment)


## software project
class Project(Module):
    def __init__(self, V=None):
        if not V: V = MODULE
        super().__init__(V)
        self.init_dirs()
        self.init_vscode()
        self.init_apt()
        self.init_files()
        self.init_test()
        #
        self.init_meta()
        self.init_links()
        self.init_readme()
        #
        self.init_src()

    def init_src(self): pass

    def init_test(self):
        self.test = Dir('test'); self.d // self.test
        self.test.giti = gitiFile(); self.test // self.test.giti

    def init_meta(self):
        self.TITLE = self.MODULE = self.value
        self.ABOUT = S()
        self.AUTHOR = 'Dmitry Ponyatov'
        self.EMAIL = 'dponyatov@gmail.com'
        self.LICENSE = 'All rights reserved'
        self.YEAR = 2021
        self.GITHUB = f'github: https://github.com/ponyatov/{self.value}'
        self.BITBUCKET = f'github: https://bitbucket.org/ponyatov/{self.value}/src/main/'

    def init_links(self):
        self.links = S('## Links')

    def init_readme(self):
        self.readme = mdFile('README'); self.d // self.readme
        self.readme \
            // f'#  `{self.MODULE}`' \
            // f'## {self.TITLE}' \
            // '' \
            // self.ABOUT \
            // '' \
            // f'(c) {self.AUTHOR} <<{self.EMAIL}>> {self.YEAR} {self.LICENSE}' \
            // '' \
            // self.GITHUB // self.BITBUCKET \
            // '' // '' \
            // self.links

    def init_apt(self):
        self.apt = File('apt', '.txt')
        self.d // (self.apt
                   // 'git make curl')
        self.dev = File('apt', '.dev')
        self.d // (self.dev
                   // 'code meld'
                   // 'sqlitebrowser pgadmin4')

    def init_vscode(self):
        self.vscode = Dir('.vscode'); self.d // self.vscode
        self.init_vscode_settings()
        self.init_vscode_tasks()
        self.init_vscode_extensions()

    def init_vscode_settings(self):
        self.vscode.settings = jsonFile('settings')
        self.vscode // self.vscode.settings

    def init_vscode_tasks(self):
        self.vscode.tasks = jsonFile('tasks')
        self.vscode // self.vscode.tasks

    def init_vscode_extensions(self):
        self.vscode.extensions = jsonFile('extensions')
        self.vscode // self.vscode.extensions
        self.vscode.ext = (S('"recommendations": [', ']')
                           // '"ryuta46.multi-command",'
                           // '"stkb.rewrap",'
                           // '"auchenberg.vscode-browser-preview",'
                           // '// "ms-azuretools.vscode-docker",'
                           // '// "tabnine.tabnine-vscode",')
        self.vscode.extensions \
            // (S('{', '}') // self.vscode.ext)

    def init_dirs(self):
        self.d = Dir(self.value); Dir('tmp') // self.d
        # bin
        self.bin = Dir('bin'); self.d // self.bin
        self.bin.giti = gitiFile(); self.bin // self.bin.giti
        # doc
        self.doc = Dir('doc'); self.d // self.doc
        self.doc.giti = gitiFile(); self.doc // (self.doc.giti // '*.pdf')
        # include
        self.include = Dir('include'); self.d // self.include
        self.include.giti = gitiFile(); self.include // self.include.giti
        # lib
        self.lib = Dir('lib'); self.d // self.lib
        self.lib.giti = gitiFile(); self.lib // self.lib.giti
        # src
        self.src = Dir('src'); self.d // self.src
        self.src.giti = gitiFile(); self.src // self.src.giti
        # tmp
        self.tmp = Dir('tmp'); self.d // self.tmp
        self.tmp.giti = gitiFile(); self.tmp // (self.tmp.giti // '*')

    def sync(self): self.d.sync()

    def init_files(self):
        self.init_giti()
        self.init_mk()

    def init_giti(self):
        self.giti = gitiFile(); self.d // self.giti
        self.giti \
            // '*~' // '*.swp' // '*.log' // '' \
            // '/docs/' // ''

    def init_mk(self):
        self.mk = Makefile(); self.d // self.mk
        self.mk \
            // (Sec('var')
                // 'MODULE  = $(notdir $(CURDIR))'
                // 'OS      = $(shell uname -s)'
                // 'MACHINE = $(shell uname -m)'
                // 'NOW     = $(shell date +%d%m%y)'
                // 'REL     = $(shell git rev-parse --short=4 HEAD)'
                // 'CORES   = $(shell grep processor /proc/cpuinfo| wc -l)'
                ) // ''
        self.mk \
            // (Sec('dir')
                // 'CWD     = $(CURDIR)'
                // 'BIN     = $(CWD)/bin'
                // 'DOC     = $(CWD)/doc'
                // 'TMP     = $(CWD)/tmp'
                // 'LIB     = $(CWD)/lib'
                // 'SRC     = $(CWD)/src'
                // 'TEST    = $(CWD)/test'
                // 'GZ      = $(HOME)/gz'
                ) // ''
        self.mk.tool = Sec('tool')
        self.mk // (self.mk.tool
                    // 'CURL    = curl -L -o'
                    ) // ''
        self.mk.src = Sec('src'); self.mk // self.mk.src // ''
        #
        self.mk.repl = S('repl:', pfx='.PHONY: repl')
        self.mk.format = S('format:', pfx='\n.PHONY: format')
        self.mk.test = S('test:', pfx='\n.PHONY: test')
        self.mk.all = Sec('all') \
            // self.mk.repl \
            // self.mk.test \
            // self.mk.format
        self.mk // self.mk.all // ''
        #
        self.mk.doc = Sec('doc'); self.mk // self.mk.doc // ''
        self.mk.install = Sec('install'); self.mk // self.mk.install
        self.mk.install // S('.PHONY: install update')
        #
        self.mk.install.install = S('install: $(OS)_install')
        self.mk.install // self.mk.install.install
        self.mk.install.body = S(); self.mk.install // self.mk.install.body
        self.mk.install // (S() // '$(MAKE) update')
        #
        self.mk.update = S('update: $(OS)_update')
        self.mk.update.body = S()
        self.mk.install // self.mk.update // self.mk.update.body
        #
        self.mk.install.linux = S(
            'Linux_install Linux_update:', pfx='\n.PHONY: Linux_install Linux_update')
        self.mk.install // (self.mk.install.linux
                            // 'sudo apt update'
                            // 'sudo apt install -u `cat apt.txt`')
        #
        self.mk.install.js = Sec('js'); self.mk.install // self.mk.install.js
        self.mk.merge = Sec('merge'); self.mk // self.mk.merge


################################################################# Python target

class pyFile(File):
    def __init__(self, V, ext='.py', comment='#'):
        super().__init__(V, ext, comment=comment)


################################################################# Erlang target

class ErlProject(Project):
    def __init__(self, V=None):
        super().__init__(V)

    def init_mk(self):
        super().init_mk()
        self.mk.tool \
            // 'REBAR   = $(HOME)/bin/rebar3' \
            // 'ERLC    = erlc' \
            // 'ERL     = erl'
        self.mk.install \
            // (Sec('erlang')
                // '.PHONY: rebar' // 'rebar: $(REBAR)'
                // (S('$(REBAR):')
                    // '$(CURL) $@ https://s3.amazonaws.com/rebar3/rebar3 && chmod +x $@'
                    // '$(REBAR) local install'))
        # // 'ln -fs $(HOME)/.cache/rebar3/bin/rebar3 $@'))
        self.mk.install.body // '$(MAKE) rebar'

    def init_links(self):
        super().init_links()
        self.links // '' // '### Erlang' // '' \
            // '* [LYSE] Хеберт Фред' \
            // '  [Изучай Erlang во имя бобра!](https://www.ozon.ru/product/izuchay-erlang-vo-imya-dobra-hebert-fred-224324511)' \
            // '  ДМК Пресс, 2019'

    def init_apt(self):
        super().init_apt()
        self.apt // 'erlang'

    def init_vscode_extensions(self):
        super().init_vscode_extensions()
        self.vscode.ext \
            // '"pgourlain.erlang",' \
            // '"jakebecker.elixir-ls",' \
            // '// "valentin.beamdasm",'


################################################################# Elixir target

class exFile(File):
    def __init__(self, V, ext='.ex', tab=' ' * 2, comment='#'):
        super().__init__(V, ext, tab=tab, comment=comment)

class exsFile(exFile):
    def __init__(self, V, ext='.exs', comment='#'):
        super().__init__(V, ext, comment=comment)

class ExProject(ErlProject):
    def __init__(self, V=None):
        super().__init__(V)
        self.mk.tool \
            // 'MIX     = mix' \
            // 'IEX     = iex'
        self.mk.update.body // '$(MIX)  deps.get'
        self.links // '' // '### Elixir' // '' \
            // '* [Sasa] Саша Юрич' \
            // '  [Elixir в действии](https://www.ozon.ru/product/elixir-v-deystvii-yurich-sasha-217051443)' \
            // '  ДМК Пресс, 2020'
        self.init_mix()
        self.init_lib()
        self.init_test()

    def init_mk(self):
        super().init_mk()
        self.mk.repl \
            // '$(IEX)  -S mix' \
            // '$(MAKE) test' \
            // '$(MAKE) format' \
            // '$(MAKE) $@'
        self.mk.format // '$(MIX)  format'
        self.mk.test // '$(MIX) test'

    def init_apt(self):
        super().init_apt()
        self.apt // 'elixir'

    def init_lib(self):
        self.init_lib_app()
        self.init_lib_ex()

    def init_lib_app(self):
        self.lib.drop()
        self.lib.mod = Dir(f'{self:l}'); self.lib // self.lib.mod
        self.lib.app = exFile('application')
        self.lib.mod // self.lib.app
        self.lib.app \
            // (S(f'defmodule {self:m}.Application do', 'end')
                // 'use Application' // ''
                // (S('def start(_type, _args) do', 'end')
                // 'children = []'
                    // 'opts = [strategy: :one_for_one, name: Expost.Supervisor]'
                    // 'Supervisor.start_link(children, opts)'
                    ))

    def init_lib_ex(self):
        self.lib.ex = exFile(f'{self:l}'); self.lib // self.lib.ex
        self.lib.ex \
            // (S(f'defmodule {self:m} do', 'end')
                // (S('def hello do', 'end') // ':world'))

    def init_test(self):
        super().init_test()
        self.test.drop()
        self.test.helper = exsFile('test_helper')
        self.test \
            // (self.test.helper
                // '# https://virviil.github.io/2016/10/26/elixir-testing-without-starting-supervision-tree/'
                // ''
                // f'Application.load(:{self:l})'
                // ''
                // (S(f'for app <- Application.spec(:{self:l}, :applications) do', 'end')
                    // (S('case app do', 'end')
                        // (S(':exsync ->') // ':skip')
                        // (S('app ->', pfx='')
                            // 'IO.inspect(app)'
                            // 'Application.ensure_all_started(app)')))
                // ''
                // 'ExUnit.start()')
        #
        self.test.exs = exsFile(f'{self.value.lower()}_test')
        self.test // self.test.exs
        self.test.exs \
            // (S('defmodule ExpostTest do', 'end')
                // 'use ExUnit.Case'
                // f'doctest {self:m}'
                // ''
                // (S('test "hello" do', 'end')
                    // f'assert {self:m}.hello() == :world'))

    def init_mix(self):
        self.mix = exsFile('mix'); self.d // self.mix
        self.mix.project = (S('def project do', 'end') // (S('[', ']')
                            // f'app: :{self:l},'
                            // f'version: "0.0.1",'
                            // f'elixir: "~> 1.11",'
                            // f'start_permanent: Mix.env() == :prod,'
                            // f'deps: deps(),'
                            // f'aliases: aliases()'))
        self.mix.app = (S('def application do', 'end') // (S('[', ']')
                        // f'mod: {{{self:m}.Application, []}},'
                        // 'applications: [:logger],'
                        // 'extra_applications: [:exsync]'))
        self.mix.deps = (S('defp deps do', 'end') // (S('[', ']')
                         // '{:exsync, "~> 0.2", only: :dev}'))
        self.mix.aliases = (S('defp aliases do', 'end')
                            // (S('[', ']')
                                // 'test: "test --no-start"'))
        self.mix \
            // (S(f'defmodule {self:m}.MixProject do', 'end')
                // 'use Mix.Project' // ''
                // self.mix.project // ''
                // self.mix.app // ''
                // self.mix.deps // ''
                // self.mix.aliases)
        self.format = exsFile('.formatter'); self.d // self.format
        self.format \
            // '[inputs: ["{mix,.formatter}.exs", "{config,lib,test}/**/*.{ex,exs}"]]'

class PhxProject(ExProject):
    def __init__(self, V=None):
        super().__init__(V)
        self.mk.install.body \
            // '$(MIX) archive.install hex phx_new 1.5.8'

    def init_apt(self):
        super().init_apt()
        self.apt // 'npm'


################################################################### system init
if __name__ == '__main__':
    if len(sys.argv) == 1:
        shell()
    elif sys.argv[1] in ['repl', 'shell']:
        shell()
        REPL()
    else:
        raise SyntaxError(sys.argv)
