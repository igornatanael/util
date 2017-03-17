'''
@Author Alysson Milanez
WHAT IS IT?
This script count the number of contracts clauses in programs 
with extension .java
HOW TO EXECUTE?
You have to execute inside the project folder, and then it will 
search inside all the sub-folders archives with these extensions
and calculate the numbers of lines of code (LOC), preconditions
(PRE), postconditions (POST), invariants (INV).
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
FORALL = "@forall"
EXIST = "@exist"
OLD = "@old"
PARAM = "@param"
BEFORE = "@before"
REQUIRES = "@requires"
PRE = "@pre"
RETURN = "@return"
ENSURES = "@ensures"
POS = "@post"
AFTER = "@after"
THROWS = "@throws"
INVAR = "@inv"
AND = "&&"
OR = "||"

mypath = os.getcwd()
directories = [x[0] for x in os.walk(mypath)]

# Function for removing string ends.
def remove_end(s):
        s = s.rstrip()
        s = s.rstrip(AND)
        s = s.rstrip(OR)
        return s

# Function for counting clauses
def count_clauses(text):
        text = remove_end(text)
        val = 0
        t = ""
        if("[" in text and "]" in text):
                open_index = text.rindex("[") # last index of the "[" 
                close_index = text.rindex("]") # last index of the "]"
                
                exp = text[(open_index+1):(close_index)] # slicing the string getting just the content in the "[ ... ]" session

                # checking the clauses 
                if(exp == ''): return val
                if(not FORALL in exp and not EXIST in exp):
                    if(AND in exp):
                        st = exp.split(AND)
                        val = len(st)
                        
                    else:
                        val +=1
                else:
                    val +=1
        return val


# Function for updating quantifiers, and old values
def count_quantifiers(s):
        global old
        global exist
        global forall
    
        #checking quantifies
        if (FORALL in s):
                forall += s.count(FORALL)
        if (EXIST in s):
                exist += s.count(EXIST)
        if (OLD in s):
                old += s.count(OLD)

def loc(fname):
    
    global pos
    global pre  
    global inv
    
    with open(fname) as f:
        content = f.readlines()
    count_com = 0
    
    for i in range(len(content)):
        if ("/*" in content[i]):
            while (i < len(content)-1):
                content[i] = content[i].rstrip()
                count_quantifiers(content[i])                       
                #checking clausules
                # postcondition
                if (ENSURES in content[i] or POS in content[i] or RETURN  in content[i] or AFTER in content[i] or THROWS in content[i]):
                        pos += count_clauses(content[i])
                        i += 1
                        while (not "@" in content[i] and not "*/" in content[i]):
                                pos += count_clauses(content[i])
                                i += 1
                        i -= 1
                                
                # precondition
                elif (REQUIRES in content[i] or PRE in content[i] or BEFORE in content[i] or PARAM in content[i]):
                        pre += count_clauses(content[i])
                        i += 1
                        while (not "@" in content[i] and not "*/" in content[i]):
                                pre += count_clauses(content[i])
                                i += 1
                        i -= 1
                # invariant
                elif INVAR in content[i]:
                    inv += count_clauses(content[i])
                    while (not "*/" in content[i]):
                            inv += count_clauses(content[i])
                            i += 1
                    i -= 1
                
                if "*/" in content[i]:
                    break
                i += 1
    
    for i in range(len(content)):
        if content[i].strip()[:2] == "//" or content[i].strip() == "":
            count_com += 1
            #print i, content[i], ":::", count_com
            #raw_input()
        elif content[i].strip()[:2] == "/*":
            while (not("*/" in content[i-1]) and i < (len(content))):
                #print i, content[i], ":::", count_com + 1
                #raw_input()
                count_com += 1
                i += 1
    count = len(content) - count_com
    return count

def counter_loc(folname):
    count = 0
    only_jml_files = [ f for f in listdir(folname) if (f[-5:] == ".java") and isfile(join(folname,f)) ]
    for i in only_jml_files:
        count += loc(folname+"/" +i)
    return count

def total_loc(folname):
    count = 0
    for i in directories:
        count += counter_loc(i)
    return count


loc = total_loc(mypath)
cjml = pre+pos+inv

myfile = open("resultsContractJDoc.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
attbr = ["LOC", "CJML", "Preconditions", "Postconditions", "Invariants", "Forall", "Exist", "Old value"]
wr.writerow(attbr)
wr.writerow([loc, cjml, pre, pos, inv, forall, exist, old])

print "LOC: " + str(loc)
print "CJML: " + str(cjml)
print "PRE: "+ str(pre)
print "POST: "+ str(pos)
print "INV: "+ str(inv)
print "FORALL: " + str(forall)
print "EXIST: " + str(exist)
print "OLD VALUE: " + str(old)
print "\nAll the values were saved in \"resultsContractJDoc.csv\" file."
raw_input()
