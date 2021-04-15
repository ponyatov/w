import config

import os, sys, re
import datetime as dt

MODULE = os.getcwd().split('/')[-1]


## base object graph node = frame
class Object:
    def __init__(self, V):
        ## scalar value: name, number, string,..
        self.value = V
        ## associative array = namespace = map
        self.slot = {}
        ## ordered container = vector = stack = queue = AST
        self.nest = []
        ## global unical id
        self.gid = id(self)


class Primitive(Object): pass

## a.k.a. atom, keyword, symbol
class Name(Primitive): pass

class String(Primitive): pass

class Number(Primitive): pass

class Integer(Number): pass

## machine hexadecimal number
class Hex(Integer): pass

## binary string
class Bin(Integer): pass


## EDS: Executable Data Structure (c)
class Active(Object): pass

## function
class Fn(Active): pass


class Meta(Object): pass

class Module(Meta): pass

class Class(Meta): pass

class Method(Meta, Fn): pass


class IO(Object): pass

class Time(IO): pass

class Path(IO): pass

class Dir(IO): pass

class File(IO): pass


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
