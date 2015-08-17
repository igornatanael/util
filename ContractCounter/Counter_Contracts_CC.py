'''
@Author Igor Natanael

WHAT IS IT?
This script count the number of clauses of contracts in programs
written in C# using the library of "CodeContracts".

HOW TO EXECUTE?
You have to execute inside the project folder, and then it will 
search inside all the sub-folders archives with these extensions
and calculate the numbers of lines of code (LOC) and lines of
CodeContracts (LOCC).
'''


import os, sys, csv
from os import listdir
from os.path import isfile, join

pos = 0
pre = 0
inv = 0
old = 0
forall = 0
exist = 0
FORALL = ".ForAll("
EXIST = ".Exist("
OLD = ".Old("
ENSURES = ".Ensures("
REQUIRES = ".Requires("	
INVAR = ".Invariant("



CONTRACT = "Contract."
aux = ""
mypath = os.getcwd()

directories = [x[0] for x in os.walk(mypath)]
    
def loc(fname):
    count = 0
    with open(fname) as f:
        content = f.readlines()

    for i in content:
        aux = i.strip()[:9]
        if aux != "" and aux != "{" and aux != "}" and aux[:2] != "//":
            count += 1
    return count

def counter_loc(folname):
    count = 0
    only_cs_files = [ f for f in listdir(folname) if (f[-3:] == ".cs") and isfile(join(folname,f)) ]
    for i in only_cs_files:
        count += loc(folname+"\\" +i)
    return count

def total_loc(folname):
    count = 0
    for i in directories:
        count += counter_loc(i)
    return count

def contracts_counter(fname):
    global pos
    global pre
    global inv
    global cons
    global old
    global exist
    global forall
    
    count = 0
	
    with open(fname) as f:
	content = f.readlines()

    for i in content:
        aux = i.strip()[:9]
        if aux == CONTRACT:
            count += 1
            if EXIST in i:
		    exist += 1
	    if FORAL in i:
		    forall += 1
	    if ENSURES in i:
		    pos += 1
	    if REQUIRES in i:
		    pre += 1
	    if OLD in i:
		    old += 1
	    if INVAR in i:
		    inv += 1
	    
		
    return count

def folder_contracts_num(folname):
    count = 0
    only_cs_files = [ f for f in listdir(folname) if (f[-3:] == ".cs") and isfile(join(folname,f)) ]
    for i in only_cs_files:
        count += contracts_counter(folname+"\\" +i)
    return count

def total_pro_contracts(folname):
    count = 0
    for i in directories:
        count += folder_contracts_num(i)
    return count

loc = total_loc(mypath)
locc = total_pro_contracts(mypath)

myfile = open("results.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
attbr = ["LOC", "LOCC", "Preconditions",  "Postconditions",  "Invariants",  "Forall", "Exist", "Old value"]
wr.writerow(attbr)
wr.writerow([loc, locc, pre,  pos,  inv, forall, exist, old])

print "LOC: " + str(loc)
print "LOCC: " + str(locc)
print "PRE: "+ str(pre)
print "POST: "+ str(pos)
print "INV: "+ str(inv)
print "FORALL: " + str(forall)
print "EXIST: " + str(exist)
print "OLD VALUE: " + str(old)
print "\nAll the values were saved in \"results.csv\" file."
raw_input()
