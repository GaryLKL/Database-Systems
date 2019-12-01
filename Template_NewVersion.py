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
	global mydata
	mydata = []

	with open(file_path) as file:
		for line in file:
			mydata.append(tuple(line.strip(" \n+").split("|")))
	
	#headers = dict(zip(mydata[0], range(len(mydata[0]))))
	
	# data types
	names = mydata[0]
	formats = ["<U10"] * len(names)
	#datatype = list(zip(names, formats))
	datatype = np.dtype({'names': names, 'formats': formats})
	#mytype = list(zip(list(headers.keys()), ["<U10"] * len(headers.keys())))
	mydata = np.array(mydata[1:], dtype = datatype)
	
	return mydata


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
		#col_index = headers.get(column_name) 
		try:
			# string to int
			mytype = [(name, int) if name == column_name else (name, tp[0]) for name, tp in table.dtype.fields.items()]
			table = np.array(table, dtype = mytype)

		except:
			pass # stay string

		#eval("[i for i, v in enumerate(mytable['time'] > 40) if v == True]")
		string_condition =  "[i for i, v in enumerate(table[column_name]" + condition.split(column_name)[1] + ") if v == True]"
		return eval(string_condition) # the index of the true condition


	
	if "and" in statemt:
		conditions = statemt.split("and")
		for con in conditions:
			table = [table[i] for i in get_remain_index(con, table)]

		return table

	elif "or" in statemt:
		remain_index_or_condition = []
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

	return [[table[col_name][line] for col_name in args] for line in range(len(table))]

def avg(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to int
		mytype = [(name, int) if name in args else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)

	except:
		print("Some of the selected columns could not be conveted to integers.")

	return [np.mean([table[col_name][line] for line in range(len(table))]) for col_name in args]

	#return [np.mean([table[line][headers.get(col_name)] for line in range(len(table))]) for col_name in args]

def sum(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to int
		mytype = [(name, int) if name in args else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)

	except:
		print("Some of the selected columns could not be conveted to integers.")
		
	return [np.sum([table[col_name][line] for line in range(len(table))]) for col_name in args]

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
		return [len([table[col_name][line] for line in range(len(table))]) for col_name in args]

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
		group_set.append(set([table[line][headers.get(col_name)] for line in table]))

	# all combinations for columns' group
	combinations = list(product(group_set))

	# initializing
	new_col_length = len(args) + 1
	group_table = [[]*(new_col_length)] # used to save the new table with the avg and other group columns

	#[table[line][headers.get(avgcol)] for line in range(len(table)) if ]


def join(tb1, tb2, by_condition):
	'''
	1. Function:  
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	def get_index(condition, tb1, tb2):
		condition = condition.strip("(\(|\)| )+") # e.g. (R1.qty > S.Q) -> R1.qty > S.Q

		tb1_col = re.split("=|<|>|!=|<=|>=", condition)[0].strip(" +").split(".")[1] # "qty"
		tb2_col = re.split("=|<|>|!=|<=|>=", condition)[1].strip(" +").split(".")[1] # "Q"

		mydelimiter = re.findall('=|<|>|!=|<=|>=', condition)[0] # ">"
		
		try:
			# string to int
			mytype1 = [(name, int) if name == tb1_col else (name, tp[0]) for name, tp in tb1.dtype.fields.items()]
			tb1 = np.array(tb1, dtype = mytype1)
		except:
			pass # stay string

		try:
			# string to int
			mytype2 = [(name, int) if name == tb2_col else (name, tp[0]) for name, tp in tb2.dtype.fields.items()]
			tb2 = np.array(tb2, dtype = mytype2)
		except:
			pass # stay string

		# start to make the comparison
		index_dict = {} # {"tb1_index": "tb2_index_list"}
		for indexone in range(len(tb1)):
			index_dict[indexone] = []
			for indextwo in range(len(tb2)):
				#eval("if tb1["+str(indexone)+"]["+str(col_index_1)+"] "+mydelimiter+" tb2["+str(indextwo)+"]["+str(col_index_2)+"]: "+"index_dict["+str(indexone)+"].append("+str(indextwo)+")")
				result_bool = eval("tb1[tb1_col][indexone] " + mydelimiter + " tb2[tb2_col][indextwo]")
				if result_bool == True:
					index_dict[indexone].append(indextwo)


		return index_dict


	final_table = []
	if "and" in by_condition:
		dict_list = []
		conditions = by_condition.split("and")
		for con in conditions:
			dict_list.append(get_index(con, tb1, tb2))

		new_dict = {}
		for line in range(len(tb1)):
			intersect = []
			for con_ind in range(len(conditions)):
				intersect.append(dict_list[con_ind][line])
			new_dict[line] = list(set(intersect[0]).intersection(*intersect))
		
		for ind_1, ind_2 in new_dict.items():
			if len(ind_2) > 0:
				for each_ind_2 in ind_2:
					final_table.append(tuple(list(tb1[ind_1]) + list(tb2[each_ind_2])))

		return final_table

	elif " or " in by_condition or ")or " in by_condition or " or(" in by_condition or ")or(" in by_condition:
		delim = re.findall(" or |\)or | or\(|\)or\(", by_condition)[0]
		dict_list = []
		conditions = by_condition.split(delim)
		for con in conditions:
			dict_list.append(get_index(con, tb1, tb2))

		new_dict = {}
		for line in range(len(tb1)):
			Union = []
			for con_ind in range(len(conditions)):
				Union.append(dict_list[con_ind][line])
			new_dict[line] = list(set().union(*Union))
		
		for ind_1, ind_2 in new_dict.items():
			if len(ind_2) > 0:
				for each_ind_2 in ind_2:
					final_table.append(tuple(list(tb1[ind_1]) + list(tb2[each_ind_2])))

		return final_table

	else:
		index_table = get_index(by_condition, tb1, tb2)
		for ind_1, ind_2 in index_table.items():
			if len(ind_2) > 0:
				for each_ind_2 in ind_2:
					final_table.append(tuple(list(tb1[ind_1]) + list(tb2[each_ind_2])))

		return final_table

	

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

