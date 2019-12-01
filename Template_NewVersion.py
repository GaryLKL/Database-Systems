import numpy as np
import re
from itertools import product 

def inputfromfile(file_path):
	'''
	1. Function: to read the data line by line 
	2. Inputs: the path of the text file whose delimiter is "|" and headers are in the first line
	3. Outputs: a n*m array data; n is the number of lines; m is the number of columns
	4. Side Effect: 
	'''
	global headers
	global mydata
	mydata = []

	with open(file_path) as file:
		for line in file:
			mydata.append(line.strip(" \n+").split("|"))
	
	headers = dict(zip(mydata[0], range(len(mydata[0]))))
	
	# data types
	# names = mydata[0]
	# formats = ["<U10"] * len(names)
	# datatype = np.dtype({'names': names, 'formats': formats})
	#mytype = list(zip(list(headers.keys()), ["<U10"] * len(headers.keys())))
	#mydata = np.array(mydata[1:], dtype = datatype)
	
	return mydata[1:]


def select(table, statemt):
	'''
	1. Function: to select all columns from the table with restricted rows under the statement
	2. Inputs: "table" means a 2-dimension array data; "statemt" is the string-type condition statement
	3. Outputs: a n*m array data
	4. Side Effect:
	'''

	def get_remain_index(condition, table):
		condition = condition.strip("(\(|\)| )+") # e.g. "(time > 50)" -> time > 50

		column_name = re.split("=|<|>|!=|<=|>=", condition)[0].strip(" +") # e.g. "time"
		col_index = headers.get(column_name) 
		try:
			# string to int
			for i in range(len(table)):
				table[i][col_index] = int(table[i][col_index])

		except:
			pass # stay string

		string_condition = "[ind for ind, line in enumerate(table) if line[" + str(col_index) + "]" + condition.split(column_name)[1] + "]"
		return eval(string_condition) # the index of the true condition


	remain_index_or_condition = []
	if "and" in statemt:
		conditions = statemt.split("and")
		for con in conditions:
			table = [table[i] for i in get_remain_index(con, table)]

		return table

	elif "or" in statemt:
		conditions = statemt.split("or")
		for con in conditions:
			remain_index_or_condition = remain_index_or_condition + get_remain_index(con, table) # e.g. [] + [1,2] + [2,3,4] -> [1,2,2,3,4]

		final_or_index = set(remain_index_or_condition) # e.g. [1,2,2,3,4] -> [1,2,3,4]

		return [table[i] for i in final_or_index]

	else:
		# only one condition
		return [table[i] for i in get_remain_index(statemt, table)]


def project(table, *args):
	'''
	1. Function: to select specific columns from the table
	2. Inputs: "table" means a 2-dimension array data; *args are the selected column names
	3. Outputs: a table with selected columns
	4. Side Effect:
	'''

	return [[table[line][headers.get(col_name)] for col_name in args] for line in range(len(table))]

def avg(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		for col_name in args:
			col_index = headers.get(col_name)
			for i in range(len(table)):
				table[i][col_index] = int(table[i][col_index])
	except:
		print("Some of the selected columns could not be conveted to integers.")

	for col_name in args:
		print(np.mean([table[line][headers.get(col_name)] for line in range(len(table))]))

	#return [np.mean([table[line][headers.get(col_name)] for line in range(len(table))]) for col_name in args]

def sum(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		for col_name in args:
			col_index = headers.get(col_name)
			for i in range(len(table)):
				table[i][col_index] = int(table[i][col_index])
	except:
		print("Some of the selected columns could not be conveted to integers.")
		
	return [[np.sum(table[line][headers.get(col_name)]) for col_name in args] for line in range(len(table))]

def count(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	if args == "*":
		return len(table)
	else:
		return [[len(table[line][headers.get(col_name)]) for col_name in args] for line in range(len(table))]

def countgroup():
	'''
	1. Function:  
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return 
	
def sumgroup():
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return


def avggroup(table, avgcol, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		col_index = headers.get(avgcol)
		for i in range(len(table)):
			table[i][col_index] = int(table[i][col_index])
	except:
		print("Some of the selected columns could not be conveted to integers.")

	# find groups for all columns
	group_set = [] 
	for col_name in args:
		group_set.append(set(table[headers.get(col_name)]))

	# all combinations for columns' group
	combinations = list(product(group_set))

	# initializing
	new_col_length = len(args) + 1
	group_table = [[]*(new_col_length)] # used to save the new table with the avg and other group columns

	table[line][headers.get(avgcol)]


def join():
	'''
	1. Function:  
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def sort():
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def movavg():
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def movsum():
	'''
	1. Function:
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def concat():
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def outputtofile():
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return 

