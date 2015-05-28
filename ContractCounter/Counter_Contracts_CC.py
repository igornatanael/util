import os
from os import listdir
from os.path import isfile, join


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
    count = 0
    with open(fname) as f:
        content = f.readlines()

    for i in content:
        aux = i.strip()[:9]
        if aux == CONTRACT:
            count += 1
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

print "LOC: " + str(total_loc(mypath))
print "LOCC: "+ str(total_pro_contracts(mypath))
raw_input()
