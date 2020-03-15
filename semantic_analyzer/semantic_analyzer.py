"""
leo kivikunnas 525925
jaakko koskela 526050
"""

#intermediate code generation is not done yet
from parser import get_addr

#import symbol table
#context stack?

#semantic stack
ss = [] #error handlin if ss is unexpectedly empty

#semantic routines

def pid(id):
    #should id be the token for type mismatch checks etc
    #get the address from the table and push that - how to do type checks 
    # push token now and get addresses later when you generate the three address code - after type checking!

    ss.append()

def add():
    first = ss.pop()
    second = ss.pop()
    #stack should not be empty
    #check both types 
    #perform addition
    #create token and push to stack
    result = first + second

def mult():
    pass

def assign():
    pass

def jpf():
    pass

def jp():
    pass

def save():
    pass

def save_jpf():
    pass



def semantic_check(action):

    if(action == "#PID"):
        pass
    elif(action == "#ADD"):
        pass
    elif(action == "#MULT"):
        pass
    elif(action == "#ASSIGN"):
        pass
    elif(action == ""):
        pass
    elif(action == ""):
        pass
    elif(action == ""):
        pass
    elif(action == ""):
        pass
    elif(action == ""):
        pass
    else:
        pass
    
