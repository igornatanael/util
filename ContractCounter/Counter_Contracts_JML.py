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

import os
from os import listdir
from os.path import isfile, join

pos = 0
pre = 0
inv = 0
cons = 0
ENSURES = "ensures"
REQUIRES = "requires"
PRE = "pre"
POS = "post"
INVAR = "invariant"
CONST = "constraint"
AT = "@"



mypath = os.getcwd()

directories = [x[0] for x in os.walk(mypath)]
    
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
			if (ENSURES in content[i] or POS in content[i]):
				pos += 1
				#print content[i]
			elif (REQUIRES in content[i] or PRE in content [i]):
				pre += 1
				#print content[i]
			elif INVAR in content[i]:
				inv += 1
				#print content[i]
			elif CONST in content[i]:
				cons += 1
				#print content[i]
		elif ((AT in content[i] and "/*" in content[i])):

			while (i < len(content)-1):
				if not("//" in content[i]):
					
					if (ENSURES in content[i] or POS in content[i]):
						pos += 1
						#print content[i]
					elif (REQUIRES in content[i] or PRE in content [i]):
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
    only_cs_files = [ f for f in listdir(folname) if (f[-5:] == ".java" or f[-4:] == ".jml" or f[-5:] == ".spec" or f[-13:] == ".java-refined" or f[-12:] == ".jml-refined") and isfile(join(folname,f)) ]
    for i in only_cs_files:
        count += loc(folname+"/" +i)
    return count

def total_loc(folname):
    
    count = 0
    for i in directories:
        count += counter_loc(i)
    return count
	
print "LOC: " + str(total_loc(mypath))
print "PRE: "+ str(pre)
print "POST: "+ str(pos)
print "INV: "+ str(inv)
print "CONS: "+ str(cons)
raw_input()
