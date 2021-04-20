import config

import os, sys, re
import datetime as dt

MODULE = os.getcwd().split('/')[-1]


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
        if isinstance(that, str): return String(that)
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

    ## @name computation

    def eval(self, env):
        raise NotImplementedError('eval', self)

    def apply(self, env, that):
        raise NotImplementedError('apply', self, that)


class Primitive(Object):
    def eval(self, env): return self
    ## source code generation

    def src(self, depth=0, to=None):
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

class Dir(IO): pass

class File(IO): pass

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
    def __init__(self, start=None, end=None):
        super().__init__(start)
        self.start = start
        self.end = end

    ## source code generation
    def src(self, depth=0, to=Console):
        ret = f'{to.tab*depth}{self.start}\n'
        for j in self.nest:
            ret += j.src(depth + 1, to) + '\n'
        ret += f'{to.tab*depth}{self.end}\n'
        return ret

## source section
class Sec(Meta): pass

class Module(Meta): pass

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
                ).src()

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

def watcher():
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


################################################################### system init


if __name__ == '__main__':
    if sys.argv[1] in ['repl', 'shell']:
        watcher()
        REPL()
    else:
        raise SyntaxError(sys.argv)
