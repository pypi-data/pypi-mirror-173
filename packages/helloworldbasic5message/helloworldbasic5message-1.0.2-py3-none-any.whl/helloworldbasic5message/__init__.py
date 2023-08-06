# description like this
# abc
# 123

try:
    from mymessage import *
except:
    print("failed import, sayhello2 function still available")

def sayhello2(name):
    result="version 5.01 hello "+name
    print(result)
    return result





