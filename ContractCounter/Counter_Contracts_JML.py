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
FORALL = "\\forall"
EXIST = "\exist"
OLD = "\old"
ENSURES = "ensures"
REQUIRES = "requires"
PRE = "pre"
POS = "post"
INVAR = "invariant"
CONST = "constraint"
AT = "@"
T = " true"



mypath = os.getcwd()
directories = [x[0] for x in os.walk(mypath)]


def loc(fname):
	
	global pos
	global pos_true
	global pre
	global pre_true
	global inv
	global cons
	global old
	global exist
	global forall
	
	with open(fname) as f:
		content = f.readlines()
        count_com = 0
	
	for i in range(len(content)):
		if (AT in content[i] and "//" in content[i]):
		
			#checking quantifies
			if (FORALL in content[i]):
				forall += 1
			if (EXIST in content[i]):
				exist += 1
			if (OLD in content[i]):
				old +=1 
					
			#checking clausules
			if (ENSURES in content[i] or POS in content[i]):
				pos += 1
				#print content[i]
				if (T in content[i]):
					pos_true += 1
			elif (REQUIRES in content[i] or PRE in content [i]):
				pre += 1
				#print content[i]
				if (T in content[i]):
					pre_true += 1
			elif INVAR in content[i]:
				inv += 1
				#print content[i]
			elif CONST in content[i]:
				cons += 1
				#print content[i]
		elif ((AT in content[i] and "/*" in content[i])):

			while (i < len(content)-1):
				if not("//" in content[i]):
					
					#checking quantifies
					if (FORALL in content[i]):
						forall += 1
					if (EXIST in content[i]):
						exist += 1
					if (OLD in content[i]):
						old +=1 
						
					#checking clausules
					if (ENSURES in content[i] or POS in content[i]):
						pos += 1
						#print content[i]
					elif (REQUIRES in content[i] or PRE in content[i]):
						pre += 1
						#print content[i]
					elif INVAR in content[i]:
						inv += 1
						#print content[i]
					elif CONST in content[i]:
						cons += 1
						#print content[i]
					
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

myfile = open("results.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
attbr = ["LOC", "Preconditions", "Pre-defauts", "Postconditions", "Post-defaults", "Invariants", "Constraints", "Forall", "Exist", "Old value"]
wr.writerow(attbr)
wr.writerow([loc, pre, pre_true, pos, pos_true, inv, cons, forall, exist, old])

print "LOC: " + str(loc)
print "PRE: "+ str(pre)
print "Preconditions true (default): " + str(pre_true)
print "POST: "+ str(pos)
print "Postconditions true (default): " + str(pos_true)
print "INV: "+ str(inv)
print "CONS: "+ str(cons)
print "FORALL: " + str(forall)
print "EXIST: " + str(exist)
print "OLD VALUE: " + str(old)
print "\nAll the values were saved in \"results.csv\" file."
raw_input()
