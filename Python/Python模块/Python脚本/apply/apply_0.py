#!/usr/bin/env python
# encoding: UTF-8

def noargs_fun():
    print "No args functions"

def tup_fun(arg1,arg2):
    print arg1, arg2

def dic_fun(arg1=1,arg2=2):
    print arg1, arg2

if __name__ == '__main__':
    apply(noargs_fun)
    apply(tup_fun,("ARG1","ARG2"))
    kw = {'arg1':'ARG1','arg2':'ARG2'}
    apply(dic_fun,(),kw)
