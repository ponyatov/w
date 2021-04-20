import pytest

from metaL import *

def test_any(): assert True


hello = Object('Hello')
def test_hello():
    assert hello.test() == '\n<object:Hello>'


world = Object('World')
def test_world():
    assert (hello // world).test() == \
        '\n<object:Hello>\n\t0: <object:World>'

def test_operators():
    left = Object('left'); right = Object('right')
    # << >>
    assert (hello << left >> right).test() == \
        '\n<object:Hello>' +\
        '\n\tobject = <object:left>' +\
        '\n\tright = <object:right>' +\
        '\n\t0: <object:World>'
    ## A[key:str]
    assert hello['right'] == right
    ## A[index:int]
    assert hello[0] == world
    ## A[key:str] = B
    some = Object(''); slot = Object('slot')
    some['slot'] = slot
    assert some.test() == '\n<object:>\n\tslot = <object:slot>'
    # ; some[0] = slot
