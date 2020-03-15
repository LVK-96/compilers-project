#import symbol table
#context stack?

#index of three address table
i = 0

#intermediate code generation - a list for now
three_address = []

#semantic stack
ss = [] #error handlin if ss is unexpectedly empty

#semantic routines

def pid(id):
    #should id be the token for type mismatch checks etc
    #get the address from the table and push that - how to do type checks 
    # push token now and get addresses later when you generate the three address code - after type checking!
    ss.append()

def add():
    first = ss.pop() #what types are these?
    second = ss.pop()
    result = first + second
    #get temp
    #type check here

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





def get_three_adress():
    #returns the three address code
    pass