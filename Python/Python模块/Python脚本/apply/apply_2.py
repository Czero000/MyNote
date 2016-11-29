#!/usr/bin/env python
# encoding: UTF-8

def function(a, b):
    print a, b

apply(function, ("Charlie", "ZeroUnix"))
apply(function, ("Charlie",), {"b": "ZeroUnix"})
apply(function, (), {"a": "Charlie", "b":"ZeroUnix"})
