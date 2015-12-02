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
                                if(ENSURES in content[i]):
                                        aux = content[i].rsplit(ENSURES)
                                        aux = aux[1]
                                        if(AND in aux):
                                                pos += len(aux.split(AND))
                                        elif(OR in aux):
                                                pos += len(aux.split(OR))
                                        else:
                                                pos += 1
                                elif(POS in content[i]):
                                        aux = content[i].rsplit(POS)
                                        aux = aux[1]
                                        if(AND in aux):
                                                pos += len(aux.split(AND))
                                        elif(OR in aux):
                                                pos += len(aux.split(OR))
                                        else:
                                                pos += 1                                
				#print content[i]
                                count_post_defaults(content[i])
			elif (REQUIRES in content[i] or PRE in content [i]):
				if(REQUIRES in content[i]):
                                        aux = content[i].rsplit(REQUIRES)
                                        aux = aux[1]
                                        if(AND in aux):
                                                pre += len(aux.split(AND))
                                        elif(OR in aux):
                                                pre += len(aux.split(OR))
                                        else:
                                                pre += 1
                                elif(PRE in content[i]):
                                        aux = content[i].rsplit(PRE)
                                        aux = aux[1]
                                        if(AND in aux):
                                                pre += len(aux.split(AND))
                                        elif(OR in aux):
                                                pre += len(aux.split(OR))
                                        else:
                                                pre += 1
				#print content[i]
				count_pre_defaults(content[i])
			elif INVAR in content[i] and "loop_invariant" not in content[i]:
				aux = content[i].rsplit(INVAR)
                                aux = aux[1]
                                if(AND in aux):
                                        inv += len(aux.split(AND))
                                elif(OR in aux):
                                        inv += len(aux.split(OR))
                                else:
                                        inv += 1
				#print content[i]
			elif CONST in content[i]:
				aux = content[i].rsplit(CONST)
                                aux = aux[1]
                                if(AND in aux):
                                        cons += len(aux.split(AND))
                                elif(OR in aux):
                                        cons += len(aux.split(OR))
                                else:
                                        cons += 1
                          
				#print content[i]
		elif ((AT in content[i] and "/*" in content[i])):

			while (i < len(content)-1):
				if not("//" in content[i]):
					
					count_quantifiers(content[i])
						
					#checking clausules
					# postcondition
					if (ENSURES in content[i] or POS in content[i]):
                                                if(ENSURES in content[i]):
                                                        count_post_defaults(content[i])
                                                        aux = content[i].rsplit(ENSURES)
                                                        aux[1] = aux[1].rstrip()
                                                        if(aux[1] != ''):
                                                                aux = aux[1]
                                                                if(AND in aux):
                                                                        pos += len(aux.split(AND))
                                                                elif(OR in aux):
                                                                        pos += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        pos += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        pos += 1
                                                        else:
                                                                i+=1
                                                                while 1:
                                                                        count_post_defaults(content[i])
                                                                        count_quantifiers(content[i])
                                                                        aux = content[i].rstrip()
                                                                        aux = aux.rstrip(AND)
                                                                        aux = aux.rstrip(OR)
                                                                        aux = aux.rstrip(LOGICIMPL)
                                                                        if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                                pos += len(aux.split(AND))
                                                                        elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                                pos += len(aux.split(OR))
                                                                        elif(LOGICIMPL in aux):
                                                                                pos += len(aux.split(LOGICIMPL))
                                                                        else:
                                                                                pos += 1
                                                                        if(";" in aux and not FORALL in aux and not EXIST in aux): break
                                                                        i+=1
                                                elif(POS in content[i]):
                                                        count_post_defaults(content[i])
                                                        aux = content[i].rsplit(POS)
                                                        aux[1] = aux[1].rstrip()
                                                        if(aux[1] != ''):
                                                                aux = aux[1]
                                                                if(AND in aux):
                                                                        pos += len(aux.split(AND))
                                                                elif(OR in aux):
                                                                        pos += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        pos += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        pos += 1
                                                        else:
                                                                i+=1
                                                                while 1:
                                                                        count_post_defaults(content[i])
                                                                        count_quantifiers(content[i])
                                                                        aux = content[i].rstrip()
                                                                        aux = aux.rstrip(AND)
                                                                        aux = aux.rstrip(OR)
                                                                        aux = aux.rstrip(LOGICIMPL)
                                                                        if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                                pos += len(aux.split(AND))
                                                                        elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                                pos += len(aux.split(OR))
                                                                        elif(LOGICIMPL in aux):
                                                                                pos += len(aux.split(LOGICIMPL))
                                                                        else:
                                                                                pos += 1
                                                                        if(";" in aux and not FORALL in aux and not EXIST in aux): break
                                                                        i+=1
                                        # precondition
					elif (REQUIRES in content[i] or PRE in content[i]):
						if(REQUIRES in content[i]):
                                                        count_pre_defaults(content[i])
                                                        aux = content[i].rsplit(REQUIRES)
                                                        aux[1] = aux[1].rstrip()
                                                        if(aux[1] != ''):
                                                                aux = aux[1]
                                                                if(AND in aux):
                                                                        pre += len(aux.split(AND))
                                                                elif(OR in aux):
                                                                        pre += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        pre += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        pre += 1
                                                        else:
                                                                i +=1
                                                                while 1:
                                                                        count_pre_defaults(content[i])
                                                                        count_quantifiers(content[i])
                                                                        aux = content[i].rstrip()
                                                                        aux = aux.rstrip(AND)
                                                                        aux = aux.rstrip(OR)
                                                                        aux = aux.rstrip(LOGICIMPL)
                                                                        if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                                pre += len(aux.split(AND))
                                                                        elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                                pre += len(aux.split(OR))
                                                                        elif(LOGICIMPL in aux):
                                                                                pre += len(aux.split(LOGICIMPL))
                                                                        else:
                                                                                pre += 1
                                                                        if(";" in aux and not FORALL in aux and not EXIST in aux): break
                                                                        i+=1
                                                elif(PRE in content[i]):
                                                        count_pre_defaults(content[i])
                                                        aux = content[i].rsplit(PRE)
                                                        aux[1] = aux[1].rstrip()
                                                        if(aux[1] != ''):
                                                                aux = aux[1]
                                                                if(AND in aux):
                                                                        pre += len(aux.split(AND))
                                                                elif(OR in aux):
                                                                        pre += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        pre += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        pre += 1
                                                        else:
                                                                i +=1
                                                                while 1:
                                                                        count_pre_defaults(content[i])
                                                                        count_quantifiers(content[i])
                                                                        aux = content[i].rstrip()
                                                                        aux = aux.rstrip(AND)
                                                                        aux = aux.rstrip(OR)
                                                                        aux = aux.rstrip(LOGICIMPL)
                                                                        if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                                pre += len(aux.split(AND))
                                                                        elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                                pre += len(aux.split(OR))
                                                                        elif(LOGICIMPL in aux):
                                                                                pre += len(aux.split(LOGICIMPL))
                                                                        else:
                                                                                pre += 1
                                                                        if(";" in aux and not FORALL in aux and not EXIST in aux): break
                                                                        i+=1
					# invariant
					elif INVAR in content[i] and "loop_invariant" not in content[i]:
                                                aux = content[i].rsplit(INVAR)
                                                aux[1] = aux[1].rstrip()
                                                if(aux[1] != ''):
                                                        aux = aux[1]
                                                        if(AND in aux):
                                                                inv += len(aux.split(AND))
                                                        elif(OR in aux):
                                                                inv += len(aux.split(OR))
                                                        elif(LOGICIMPL in aux):
                                                                inv += len(aux.split(LOGICIMPL))
                                                        else:
                                                                inv += 1
                                                else :
                                                        i +=1
                                                        while 1:
                                                                count_quantifiers(content[i])
                                                                aux = content[i].rstrip()
                                                                aux = aux.rstrip(AND)
                                                                aux = aux.rstrip(OR)
                                                                aux = aux.rstrip(LOGICIMPL)
                                                                if("*/" in aux and AT in aux): break
                                                                if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                        inv += len(aux.split(AND))
                                                                elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                        inv += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        inv += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        inv += 1
                                                                i+=1
                                        # constraint
					elif CONST in content[i]:
						aux = content[i].rsplit(CONST)
						aux[1] = aux[1].rstrip()
                                                if(aux[1] != ''):
                                                        aux = aux[1]
                                                        if(AND in aux):
                                                                cons += len(aux.split(AND))
                                                        elif(OR in aux):
                                                                cons += len(aux.split(OR))
                                                        elif(LOGICIMPL in aux):
                                                                cons += len(aux.split(LOGICIMPL))
                                                        else:
                                                                cons += 1
                                                else:
                                                        i += 1
                                                        while 1:
                                                                count_quantifiers(content[i])
                                                                aux = content[i].rstrip()
                                                                aux = aux.rstrip(AND)
                                                                aux = aux.rstrip(OR)
                                                                aux = aux.rstrip(LOGICIMPL)
                                                                if("*/" in aux and AT in aux): break
                                                                if(AND in aux and not FORALL in aux and not EXIST in aux):
                                                                        cons += len(aux.split(AND))
                                                                elif(OR in aux and not FORALL in aux and not EXIST in aux):
                                                                        cons += len(aux.split(OR))
                                                                elif(LOGICIMPL in aux):
                                                                        cons += len(aux.split(LOGICIMPL))
                                                                else:
                                                                        cons += 1
                                                                i+=1
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
