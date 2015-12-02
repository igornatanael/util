'''
@Author Igor Natanael and Alysson Milanez
WHAT IS IT?
This script count the number of clauses of contracts in programs 
with extension .java, .jml, .spec, .java-refined and jml-refined.
HOW TO EXECUTE?
You have to execute inside the project folder, and then it will 
search inside all the sub-folders archives with these extensions
and calculate the numbers of lines of code (LOC), preconditions
(PRE), postconditions (POST), invariants (INV), and constraints (CONS).
'''

import os, sys, csv
from os import listdir
from os.path import isfile, join

pos = 0
pos_true = 0
pre = 0
pre_true = 0
inv = 0
cons = 0
old = 0
forall = 0
exist = 0
logic_impl = 0
FORALL = "\\forall"
EXIST = "\exist"
OLD = "\old"
LOGICIMPL = "==>"
ENSURES = "ensures"
REQUIRES = "requires"
PRE = "pre"
POS = "post"
INVAR = "invariant"
CONST = "constraint"
AT = "@"
T = " true"
AND = "&&"
OR = "||"

mypath = os.getcwd()
directories = [x[0] for x in os.walk(mypath)]

# Function for removing string ends.
def remove_end(s):
        s = s.rstrip()
        s = s.rstrip(AND)
        s = s.rstrip(OR)
        s = s.rstrip(LOGICIMPL)
        return s

# Function for counting clauses
def count_clauses(text, key):
        text = remove_end(text)
        val = 0
        t = ""
        if(key in text):
                t = text.rsplit(key)
                t = t[1]
                if(t == ''): return val
                if(not FORALL in t and not EXIST in t):
                        if(AND in t):
                                val += len(t.split(AND))
                        elif(OR in t):
                                val += len(t.split(OR))
                        elif(LOGICIMPL in t):
                                val += len(t.split(LOGICIMPL))
                        else:
                                val +=1
                else:
                        val +=1
        return val


# Function for updating quantifiers, old and logic impl values
def count_quantifiers(s):
        global old
	global exist
	global forall
	global logic_impl
	
        #checking quantifies
        if (FORALL in s):
		forall += s.count(FORALL)
	if (EXIST in s):
		exist += s.count(EXIST)
	if (OLD in s):
		old += s.count(OLD)
	if (LOGICIMPL in s):
                logic_impl += s.count(LOGICIMPL)

def count_pre_defaults(s):
        global pre_true
        if (T in s):
                pre_true += s.count(T)

def count_post_defaults(s):
        global pos_true
        if (T in s):
                pos_true += s.count(T)       

def loc(fname):
	
	global pos
	global pre	
	global inv
	global cons
	
	with open(fname) as f:
		content = f.readlines()
        count_com = 0
	
	for i in range(len(content)):
		if (AT in content[i] and "//" in content[i]):
			count_quantifiers(content[i])
			#checking clausules
			if (ENSURES in content[i] or POS in content[i]):
                                count_post_defaults(content[i])
                                pos += count_clauses(content[i], ENSURES)
                                pos += count_clauses(content[i], POS)                                
			elif (REQUIRES in content[i] or PRE in content [i]):
                                count_pre_defaults(content[i])
                                pre += count_clauses(content[i], REQUIRES)
                                pre += count_clauses(content[i], PRE)
			elif INVAR in content[i] and "loop_invariant" not in content[i]:
				inv += count_clauses(content[i], INVAR)
			elif CONST in content[i]:
				cons += count_clauses(content[i], CONST)

		elif ((AT in content[i] and "/*" in content[i])):
			while (i < len(content)-1):
				if not("//" in content[i]):					
					count_quantifiers(content[i])						
					#checking clausules
					# postcondition
					if (ENSURES in content[i] or POS in content[i]):
                                                count_post_defaults(content[i])
                                                pos += count_clauses(content[i], ENSURES)
                                                pos += count_clauses(content[i], POS)
                                                if(not ";" in content[i]):
                                                        while 1:
                                                                i+=1
                                                                if("*/" in content[i] and AT in content[i]): break
                                                                count_post_defaults(content[i])
                                                                count_quantifiers(content[i])
                                                                pos += count_clauses(content[i], AT)
                                                                if(";" in content[i] and not FORALL in content[i] and not EXIST in content[i]): break

                                        # precondition
					elif (REQUIRES in content[i] or PRE in content[i]):
                                                count_pre_defaults(content[i])
                                                pre += count_clauses(content[i], REQUIRES)
                                                pre += count_clauses(content[i], PRE)
                                                if(not ";" in content[i]):
                                                        while 1:
                                                                i +=1
                                                                if("*/" in content[i] and AT in content[i]): break
                                                                count_pre_defaults(content[i])
                                                                count_quantifiers(content[i])
                                                                pre += count_clauses(content[i], AT)
                                                                if(";" in content[i] and not FORALL in content[i] and not EXIST in content[i]): break
                                                        
					# invariant
					elif INVAR in content[i] and "loop_invariant" not in content[i]:
                                                inv += count_clauses(content[i], INVAR)
                                                if(not ";" in content[i]):
                                                        while 1:
                                                                i+=1
                                                                if("*/" in content[i] and AT in content[i]): break
                                                                count_quantifiers(content[i])
                                                                inv += count_clauses(content[i], AT)
                                        # constraint
					elif CONST in content[i]:
                                                cons += count_clauses(content[i], CONST)
                                                if(not ";" in content[i]):
                                                        while 1:
                                                                i+=1
                                                                if("*/" in content[i] and AT in content[i]): break
                                                                count_quantifiers(content[i])
                                                                cons += count_clauses(content[i], AT)
                                                                
				if "*/" in content[i] and AT in content[i]:
					break
				
				i += 1
	
	for i in range(len(content)):
		if content[i].strip()[:2] == "//" or content[i].strip() == "":
			count_com += 1
			#print i, content[i], ":::", count_com
			#raw_input()
		elif content[i].strip()[:2] == "/*" and not("spec_public" in content[i]):
			while (not("*/" in content[i-1]) and i < (len(content))):
				#print i, content[i], ":::", count_com + 1
				#raw_input()
				count_com += 1
				i += 1
	count = len(content) - count_com
	#print len(content), count_com
	return count

def counter_loc(folname):
    count = 0
    only_jml_files = [ f for f in listdir(folname) if (f[-5:] == ".java" or f[-4:] == ".jml" or f[-5:] == ".spec" or f[-13:] == ".java-refined" or f[-12:] == ".jml-refined") and isfile(join(folname,f)) ]
    for i in only_jml_files:
        count += loc(folname+"/" +i)
    return count

def total_loc(folname):
    count = 0
    for i in directories:
        count += counter_loc(i)
    return count


loc = total_loc(mypath)
cjml = pre+pos+inv+cons

myfile = open("results.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
attbr = ["LOC", "CJML", "Preconditions", "Pre-defaults", "Postconditions", "Post-defaults", "Invariants", "Constraints", "Forall", "Exist", "Old value", "Logic Impl"]
wr.writerow(attbr)
wr.writerow([loc, cjml, pre, pre_true, pos, pos_true, inv, cons, forall, exist, old, logic_impl])

print "LOC: " + str(loc)
print "CJML: " + str(cjml)
print "PRE: "+ str(pre)
print "Preconditions true: " + str(pre_true)
print "POST: "+ str(pos)
print "Postconditions true: " + str(pos_true)
print "INV: "+ str(inv)
print "CONS: "+ str(cons)
print "FORALL: " + str(forall)
print "EXIST: " + str(exist)
print "OLD VALUE: " + str(old)
print "LOGIC IMPL: "+ str(logic_impl)
print "\nAll the values were saved in \"results.csv\" file."
raw_input()
