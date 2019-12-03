import numpy as np
import re
from itertools import product
# The following packages are used for BTree
import ZODB 
from BTrees.OOBTree import BTree


def inputfromfile(file_path):
	'''
	1. Function: to read the data line by line 
	2. Inputs: the path of the text file whose delimiter is "|" and headers are in the first line
	3. Outputs: a array data with string-type columns;
	4. Side Effect: the function will create a global array data and also return the array
	'''
	global mydata
	mydata = []

	with open(file_path) as file:
		for line in file:
			mydata.append(tuple(line.strip(" \n+").split("|")))
	
	#headers = dict(zip(mydata[0], range(len(mydata[0]))))
	
	# data types
	names = mydata[0]
	#formats = ["<U10"] * len(names)
	#datatype = list(zip(names, formats))
	#datatype = np.dtype({'names': names, 'formats': formats})
	datatype = [(col_name, "<U10") for col_name in names]
	#mytype = list(zip(list(headers.keys()), ["<U10"] * len(headers.keys())))
	mydata = np.array(mydata[1:], dtype = datatype)
	
	return mydata


def select(table, statemt):
	'''
	1. Function: to select all columns from the table with the conditional rows under the statement
	2. Inputs: "table" means a 2-dimension array data; "statemt" is the string-type condition statement
	3. Outputs: a string-type array data with the conditional rows
	4. Side Effect: if the column is an index, the function will automatically use the btree or hash attribute
	'''


	def get_remain_index(condition, table):
		condition = condition.strip("(\(|\)| )+") # e.g. "(time + 5 > 50)" -> time > 50 / "(50 < time + 5)"

		# Is there an arithop?
		try:
			arithop = re.findall("\+|\-|\*|\/", condition)[0]
		except:
			arithop = None
			pass

		delim = re.findall("=|<|>|!=|<=|>=", condition)[0] # e.g. ">"

		# How to automatically know if the column is on the left side or right side?
		# By transform the left side to a float type, if it doesn't work, that's a column name.
		
		leftside =  condition.split(delim)[0].strip(" +") # "time + 5 > 50" -> "time + 5"
		if arithop:
			try:
				value_left = float(leftside) # "50 < time + 5"
				# The left side is a float-type value. Then, the right side has the column
				rightside = condition.split(delim)[1].strip(" +") # "time + 5"
				column_name = rightside.split(arithop)[0].strip(" +") # "time"
				number = leftside # 50
				arithop_value = rightside.split(arithop)[1].strip(" +") # 5

			except:
				value_left = None # "time + 5 > 50"
				# Then, the left side has the column
				column_name = leftside.split(arithop)[0].strip(" +") # time
				number = condition.split(delim)[1].strip(" +") # 50
				arithop_value = leftside.split(arithop)[1].strip(" +") # 5

			# Math
				if arithop == "+":
					number = str(float(number) - float(arithop_value)) # str(50 - 5)
				elif arithop == "-":
					number = str(float(number) + float(arithop_value)) # str(50 + 5)
				elif arithop == "*":
					number = str(float(number) / float(arithop_value)) # str(50 / 5)
				elif arithop == "/":
					number = str(float(number) * float(arithop_value)) # str(50 * 5)
		else:
			try:
				value_left = float(leftside) # "50 < time"
				column_name = condition.split(delim)[1].strip(" +") # e.g. "time"
				number = leftside
			except:
				value_left = None # "time > 50"
				column_name = leftside
				number = condition.split(delim)[1].strip(" +")
		
		if value_left is None:
			delim_number = delim + " '" + number + "'" # conditions one: "> '50'"
		else:
			delim_number = "'" + number + "' " + delim # conditions two: "'50' <"

		# Change the type of the column from string to float
		'''
		try:
			# string to int
			mytype = [(name, int) if name == column_name else (name, tp[0]) for name, tp in table.dtype.fields.items()]
			table = np.array(table, dtype = mytype)

		except:
			pass # stay string
		'''

		# Check if the column is an index of btree
		try:
			# The column is an index
			if column_name+"_index" in globals():
				print("aaaa")
				remain_index = []
				unique_keys = eval("list("+column_name+"_index.keys())")

				# Handle "> '50'" or "'50' <"
				if value_left is None: # conditions one: "> '50'"
					keys_under_condition = eval("[i for i in unique_keys if i"+delim_number+"]")
				else: # conditions two: "'50' <"
					keys_under_condition = eval("[i for i in unique_keys if " + delim_number + " i]")
				for i in keys_under_condition:
					remain_index = remain_index + eval(column_name+"_index.get(i)")
				return remain_index
			# The column is not an index
			else:
				if value_left is None: # conditions one: "> '50'"
					remain_index = "[i for i, v in enumerate(table[column_name] " + delim_number + ") if v == True]"
				else: # conditions two: "'50' <"
					remain_index = "[i for i, v in enumerate(" + delim_number + " table[column_name]) if v == True]"
				return eval(remain_index) # the index of the true condition
		except:
			print("Some errors may happen in your btree or hash format.")


	table_type = table.dtype
	if " and " in statemt or ")and " in statemt or " and(" in statemt or ")and(" in statemt:
		delim = re.findall(" and |\)and | and\(|\)and\(", statemt)[0]
		conditions = statemt.split(delim)

		for con in conditions:
			table = np.array([table[i] for i in get_remain_index(con, table)], dtype = table_type)

	elif " or " in statemt or ")or " in statemt or " or(" in statemt or ")or(" in statemt:
		remain_index_or_condition = []
		delim = re.findall(" or |\)or | or\(|\)or\(", statemt)[0]
		conditions = statemt.split(delim)
		for con in conditions:
			remain_index_or_condition = remain_index_or_condition + get_remain_index(con, table) # e.g. [] + [1,2] + [2,3,4] -> [1,2,2,3,4]

		final_or_index = set(remain_index_or_condition) # e.g. [1,2,2,3,4] -> [1,2,3,4]

		table = np.array([table[i] for i in final_or_index], dtype = table_type)

	else:
		# only one condition
		table = np.array([table[i] for i in get_remain_index(statemt, table)], dtype = table_type)

	# give the column name and data type to the array

	return table


def project(table, *args):
	'''
	1. Function: to select specific columns from the table
	2. Inputs: "table" means a 2-dimension array data; *args are the selected column names
	3. Outputs: a table with selected columns
	4. Side Effect:
	'''
	cols = [col_name for col_name in args]

	
	return table[cols]


def avg(table, col_name):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to float
		mytype = [(name, float) if name == col_name else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)

	except:
		print("Some of the selected columns could not be conveted to integers.")

	#cols = [col_name for col_name in args]
	#col_mean = tuple([np.mean([table[col_name][line] for line in range(len(table))]) for col_name in args])
	#datatype = [(col, float) for col in cols]
	#return np.array(col_mean, dtype = datatype)
	return np.mean([table[col_name][line] for line in range(len(table))])


def sum(table, col_name):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to float
		mytype = [(name, float) if name == col_name else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)

	except:
		print("Some of the selected columns could not be conveted to integers.")
	
	#cols = [col_name for col_name in args]
	#col_mean = tuple([np.sum([table[col_name][line] for line in range(len(table))]) for col_name in args])
	#datatype = [(col, float) for col in cols]
	#return np.array(col_mean, dtype = datatype)
	return np.sum([table[col_name][line] for line in range(len(table))])

def count(table, col_name):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	#cols = [col_name for col_name in args]
	#col_count = tuple([len(table[col_name]) for col_name in args])
	#datatype = [(col, float) for col in cols]
	#return np.array(col_count, dtype = datatype)

	return len(table[col_name])

def countgroup(table, countcol, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	
	'''
	try:
		# string to float
		mytype = [(name, float) if name == countcol else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)
	except:
		print("The selected columns could not be conveted to float.")
	'''

	# find groups for all columns
	group_set = []
	for col_name in args:
		group_set.append(list(set(table[col_name])))
	

	# all combinations for columns' group
	if len(args) == 1:
		combinations = group_set[0]
	else:
		combinations = list(product(*group_set))
	# initializing
	group_table = [] # used to save the new table with the avg and other group columns
	for comb in combinations:

		temp_ind = []
		for line in range(len(table)):
			true_false_list = []
			for i in range(len(args)):
				if table[args[i]][line] == comb[i]:
					true_false_list.append(1) # to see if this line matches all the value in comb
			if np.sum(true_false_list) == len(args):
				temp_ind.append(line) # if every value matches, append the line index into a list

		# count length
		total_number = len([table[countcol][i] for i in temp_ind])
		if len(args) == 1 and total_number != 0:
			group_table.append(tuple([total_number] + [comb])) # can't use list because list('123') -> ['1', '2', '3']
		elif len(args) > 1 and total_number != 0:
			group_table.append(tuple([total_number] + list(comb)))

	# column names and data type
	cols = [col_name for col_name in args]
	datatype = [(GroupCount, float)] + [(col, "<U10") for col in cols]

	return np.array(group_table, dtype = datatype)
	
def sumgroup(table, sumcol, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to float
		mytype = [(name, float) if name == sumcol else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)
	except:
		print("The selected columns could not be conveted to float.")

	# find groups for all columns
	group_set = []
	for col_name in args:
		group_set.append(list(set(table[col_name])))
	

	# all combinations for columns' group
	if len(args) == 1:
		combinations = group_set[0]
	else:
		combinations = list(product(*group_set))
	# initializing
	group_table = [] # used to save the new table with the avg and other group columns
	for comb in combinations:

		temp_ind = []
		for line in range(len(table)):
			true_false_list = []
			for i in range(len(args)):
				if table[args[i]][line] == comb[i]:
					true_false_list.append(1) # to see if this line matches all the value in comb
			if np.sum(true_false_list) == len(args):
				temp_ind.append(line) # if every value matches, append the line index into a list

		# count summation
		summation = np.sum([table[sumcol][i] for i in temp_ind])
		if len(args) == 1 and summation != 0:
			group_table.append(tuple([summation] + [comb])) # can't use list because list('123') -> ['1', '2', '3']
		elif len(args) > 1 and summation != 0:
			group_table.append(tuple([summation] + list(comb)))
	
	# column names and data type
	cols = [col_name for col_name in args]
	datatype = [(GroupSum, float)] + [(col, "<U10") for col in cols]

	return np.array(group_table, dtype = datatype)


def avggroup(table, avgcol, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	try:
		# string to float
		mytype = [(name, float) if name == avgcol else (name, tp[0]) for name, tp in table.dtype.fields.items()]
		table = np.array(table, dtype = mytype)
	except:
		print("The selected columns could not be conveted to integers.")

	# find groups for all columns
	group_set = []
	for col_name in args:
		group_set.append(list(set(table[col_name])))
	
	'''
	# How many combinations?
	total_combination_length = 1
	for i in group_set:
		total_combination_length = total_combination_length * len(i)
	# get all combinations
	#all_combination = [[] * total_combination_length]
	all_combination = []
	for i in range(len(args)):
		for j in group_set:
			group_length = len(j)
	'''

	# all combinations for columns' group
	if len(args) == 1:
		combinations = group_set[0]
	else:
		combinations = list(product(*group_set))
	# initializing
	group_table = [] # used to save the new table with the avg and other group columns
	for comb in combinations:

		temp_ind = []
		for line in range(len(table)):
			true_false_list = []
			for i in range(len(args)):
				if table[args[i]][line] == comb[i]:
					true_false_list.append(1) # to see if this line matches all the value in comb
			if np.sum(true_false_list) == len(args):
				temp_ind.append(line) # if every value matches, append the line index into a list

		# count average
		avg = np.mean([table[avgcol][i] for i in temp_ind])
		if len(args) == 1 and not np.isnan(avg):
			group_table.append(tuple([avg] + [comb])) # can't use list because list('123') -> ['1', '2', '3']
		elif len(args) > 1 and not np.isnan(avg):
			group_table.append(tuple([avg] + list(comb)))
	
	# column names and data type
	cols = [col_name for col_name in args]
	datatype = [(GroupAVG, float)] + [(col, "<U10") for col in cols]

	return np.array(group_table, dtype = datatype)

def join(tb1, tb2, by_condition):
	'''
	1. Function:  
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	def get_index(condition, tb1, tb2):
		condition = condition.strip("(\(|\)| )+") # e.g. (R1.qty > S.Q) -> R1.qty > S.Q

		mydelimiter = re.findall('=|<|>|!=|<=|>=', condition)[0] # ">"
		
		# Is there an arithop? e.g. (R.qty + 5 = S.time * 2)
		try:
			arithop_left = re.findall("\+|\-|\*|\/", condition.split(mydelimiter)[0])[0] # "+"
		except:
			arithop_left = None
			pass
		try:
			arithop_right = re.findall("\+|\-|\*|\/", condition.split(mydelimiter)[1])[0] # "*"
		except:
			arithop_right = None
			pass

		# How to automatically know if the column is on the left side or right side?
		# By transform the left side to a float type, if it doesn't work, that's a column name.
		if arithop_left: # R.qty + 5
			tb1_col = re.split("=|<|>|!=|<=|>=", condition)[0].split(arithop_left)[0].strip(" +").split(".")[1]
			tb1_number = re.split("=|<|>|!=|<=|>=", condition)[0].split(arithop_left)[1].strip(" +")
		else:
			tb1_col = re.split("=|<|>|!=|<=|>=", condition)[0].strip(" +").split(".")[1] # "qty"
		
		if arithop_right:
			tb2_col = re.split("=|<|>|!=|<=|>=", condition)[1].split(arithop_right)[0].strip(" +").split(".")[1]
			tb2_numbert = re.split("=|<|>|!=|<=|>=", condition)[1].split(arithop_right)[1].strip(" +")
		else:
			tb2_col = re.split("=|<|>|!=|<=|>=", condition)[1].strip(" +").split(".")[1] # "Q"


		'''
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
		'''

		key_dict = {} #{"tb1_key": "tb2_key_list"}
		index_dict = {} # {"tb1_index": "tb2_index_list"}
		if mydelimiter == "=":
			mydelimiter = "=="
			if tb1_col+"_index" in globals() and tb2_col+"_index" in globals():
				unique_keys_1 = eval("list("+tb1_col+"_index.keys())") # [1,2,3]
				unique_keys_2 = eval("list("+tb2_col+"_index.keys())") # [2,3,4]

				# do math -> [(original value, transformed value)]
				if arithop_left:
					original_transformed_key_1 = eval("[(i, float(i)" + arithop_left + tb1_number + ") for i in unique_keys_1]")
				else:
					original_transformed_key_1 = [(i, float(i)) for i in unique_keys_1]

				if arithop_right:
					original_transformed_key_2 = eval("[(i, float(i)" + arithop_right + tb2_number + ") for i in unique_keys_2]")
				else:
					original_transformed_key_2 = [(i, float(i)) for i in unique_keys_2]

				# find intersection by the transformed key and then return the original key
				for i, k in original_transformed_key_1:
					key_dict[i] = []
					for p, q in original_transformed_key_2:
						if k == q:
							key_dict[i].append(p) # #{"tb1_original_key": "tb2_original_key_list"}
				key1 = [ele for ele, ls in key_dict.items() if ls] # don't care about empty list e.g. {"tb1_original_key": []}
				for m in key1:
					for n in eval(tb1_col+"_index.get(m)"):
						index_dict[n] = []
						for k2 in key_dict[m]: # key_dict[m] is a key 2 list
							index_dict[n] = index_dict[n] + eval(tb2_col+"_index.get(k2)")

			elif tb1_col+"_index" in globals() and not tb2_col+"_index" in globals():
				unique_keys_1 = eval("list("+tb1_col+"_index.keys())")
				unique_keys_2 = list(set(tb2[tb2_col]))

				# do math -> [(original value, transformed value)]
				if arithop_left:
					original_transformed_key_1 = eval("[(i, float(i)" + arithop_left + tb1_number + ") for i in unique_keys_1]")
				else:
					original_transformed_key_1 = [(i, float(i)) for i in unique_keys_1]

				if arithop_right:
					original_transformed_key_2 = eval("[(i, float(i)" + arithop_right + tb2_number + ") for i in unique_keys_2]")
				else:
					original_transformed_key_2 = [(i, float(i)) for i in unique_keys_2]

				# find intersection by the transformed key and then return the original key
				for i, k in original_transformed_key_1:
					key_dict[i] = []
					for p, q in original_transformed_key_2:
						if k == q:
							key_dict[i].append(p) # #{"tb1_original_key": "tb2_original_key_list"}
				key1 = [ele for ele, ls in key_dict.items() if ls] # don't care about empty list e.g. {"tb1_original_key": []}
				for m in key1:
					for n in eval(tb1_col+"_index.get(m)"):
						index_dict[n] = [ind for ind, val in enumerate(tb2[tb2_col]) if val in list(key_dict[m])]

			elif not tb1_col+"_index" in globals() and tb2_col+"_index" in globals():
				unique_keys_1 = list(set(tb1[tb1_col]))
				unique_keys_2 = eval("list("+tb2_col+"_index.keys())")

				# do math -> [(original value, transformed value)]
				if arithop_left:
					original_transformed_key_1 = eval("[(i, float(i)" + arithop_left + tb1_number + ") for i in unique_keys_1]")
				else:
					original_transformed_key_1 = [(i, float(i)) for i in unique_keys_1]

				if arithop_right:
					original_transformed_key_2 = eval("[(i, float(i)" + arithop_right + tb2_number + ") for i in unique_keys_2]")
				else:
					original_transformed_key_2 = [(i, float(i)) for i in unique_keys_2]

				# find intersection by the transformed key and then return the original key
				for i, k in original_transformed_key_1:
					key_dict[i] = []
					for p, q in original_transformed_key_2:
						if k == q:
							key_dict[i].append(p) # #{"tb1_original_key": "tb2_original_key_list"}
				key1 = [ele for ele, ls in key_dict.items() if ls] # don't care about empty list e.g. {"tb1_original_key": []}
				for m in key1:
					tb1_match_ind = [ind for ind, val in enumerate(tb1[tb1_col]) if val == m]
					for n in tb1_match_ind:
						index_dict[n] = []
						for k2 in key_dict[m]: # key_dict[m] is a key 2 list
							index_dict[n] = index_dict[n] + eval(tb2_col+"_index.get(k2)")

			else:
				unique_keys_1 = list(set(tb1[tb1_col]))
				unique_keys_2 = list(set(tb2[tb2_col]))
				
				# do math -> [(original value, transformed value)]
				if arithop_left:
					original_transformed_key_1 = eval("[(i, float(i)" + arithop_left + tb1_number + ") for i in unique_keys_1]")
				else:
					original_transformed_key_1 = [(i, float(i)) for i in unique_keys_1]

				if arithop_right:
					original_transformed_key_2 = eval("[(i, float(i)" + arithop_right + tb2_number + ") for i in unique_keys_2]")
				else:
					original_transformed_key_2 = [(i, float(i)) for i in unique_keys_2]

				# find intersection by the transformed key and then return the original key
				for i, k in original_transformed_key_1:
					key_dict[i] = []
					for p, q in original_transformed_key_2:
						if k == q:
							key_dict[i].append(p) # #{"tb1_original_key": "tb2_original_key_list"}
				key1 = [ele for ele, ls in key_dict.items() if ls] # don't care about empty list e.g. {"tb1_original_key": []}
				for m in key1: 
					tb1_match_ind = [ind for ind, val in enumerate(tb1[tb1_col]) if val == m]
					for n in tb1_match_ind:
						index_dict[n] = [ind for ind, val in enumerate(tb2[tb2_col]) if val in list(key_dict[m])]
		else:
			unique_keys_1 = list(set(tb1[tb1_col]))
			unique_keys_2 = list(set(tb2[tb2_col]))
			
			# do math -> [(original value, transformed value)]
			if arithop_left:
				original_transformed_key_1 = eval("[(i, float(i)" + arithop_left + tb1_number + ") for i in unique_keys_1]")
			else:
				original_transformed_key_1 = [(i, float(i)) for i in unique_keys_1]

			if arithop_right:
				original_transformed_key_2 = eval("[(i, float(i)" + arithop_right + tb2_number + ") for i in unique_keys_2]")
			else:
				original_transformed_key_2 = [(i, float(i)) for i in unique_keys_2]

			# find intersection by the transformed key and then return the original key
			for i, k in original_transformed_key_1:
				key_dict[i] = []
				for p, q in original_transformed_key_2:
					if k == q:
						key_dict[i].append(p) # #{"tb1_original_key": "tb2_original_key_list"}
			key1 = [ele for ele, ls in key_dict.items() if ls] # don't care about empty list e.g. {"tb1_original_key": []}
			for m in key1:
				tb1_match_ind = [ind for ind, val in enumerate(tb1[tb1_col]) if val == m]
				for n in tb1_match_ind:
					index_dict[n] = [ind for ind, val in enumerate(tb2[tb2_col]) if val in list(key_dict[m])]
			'''
			# the comparison symbol is not "="
			for indexone in range(len(tb1)):
				index_dict[indexone] = []
				for indextwo in range(len(tb2)):
					#eval("if tb1["+str(indexone)+"]["+str(col_index_1)+"] "+mydelimiter+" tb2["+str(indextwo)+"]["+str(col_index_2)+"]: "+"index_dict["+str(indexone)+"].append("+str(indextwo)+")")
					result_bool = eval("tb1[tb1_col][indexone] " + mydelimiter + " tb2[tb2_col][indextwo]")
					if result_bool == True:
						index_dict[indexone].append(indextwo)
			'''

		return index_dict


	final_table = []
	if " and " in by_condition or ")and " in by_condition or " and(" in by_condition or ")and(" in by_condition:
		delim = re.findall(" and |\)and | and\(|\)and\(", by_condition)[0]
		dict_list = []
		conditions = by_condition.split(delim)

		# get the two tables name
		condition_for_table_name = conditions[0].strip("(\(|\)| )+")

		table_one_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[0].strip(" +").split(".")[0]
		table_two_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

		# start
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

	elif " or " in by_condition or ")or " in by_condition or " or(" in by_condition or ")or(" in by_condition:
		delim = re.findall(" or |\)or | or\(|\)or\(", by_condition)[0]
		dict_list = []
		conditions = by_condition.split(delim)

		# get the two tables name
		condition_for_table_name = conditions[0].strip("(\(|\)| )+")

		table_one_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[0].strip(" +").split(".")[0]
		table_two_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

		# start
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

	else:
		# get the two tables name
		condition_for_table_name = by_condition.strip("(\(|\)| )+")
		table_one_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[0].strip(" +").split(".")[0]
		table_two_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

		# start
		index_table = get_index(by_condition, tb1, tb2)
		print(index_table.items())
		for ind_1, ind_2 in index_table.items():
			if len(ind_2) > 0:
				for each_ind_2 in ind_2:
					final_table.append(tuple(list(tb1[ind_1]) + list(tb2[each_ind_2])))

	# give column name and data type to the array
	table_one_col_name = [table_one_name + "_" + i for i in tb1.dtype.names]
	table_two_col_name = [table_two_name + "_" + i for i in tb2.dtype.names]
	full_table_col_name = table_one_col_name + table_two_col_name

	#formats = ["<U10"] * len(full_table_col_name)
	#datatype = np.dtype({'names': full_table_col_name, 'formats': formats})
	datatype = [(col_name, "<U10") for col_name in full_table_col_name]
	return np.array(final_table, dtype = datatype)

	

def sort(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	sort_cols = [col_name for col_name in args]

	table_to_sort = table.copy()
	table_to_sort.sort(order = sort_cols)

	return table_to_sort

def movavg(table, col_name, n_item):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	target_col = table[col_name]
	movavg_result = []
	# first n_item-1 
	for i in range(1, n_item):
		movavg_result.append(np.mean(target_col[:i]))

	# n_item moving window
	start = 0
	while start + n_item <= len(target_col):
		movavg_result.append(np.mean(target_col[start:n_item]))
		start += 1

	return np.array(movavg_result)

def movsum(table, col_name, n_item):
	'''
	1. Function:
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''
	
	target_col = table[col_name]
	movsum_result = []
	# first n_item-1 
	for i in range(1, n_item):
		movsum_result.append(np.sum(target_col[:i]))

	# n_item moving window
	start = 0
	while start + n_item <= len(target_col):
		movsum_result.append(np.sum(target_col[start:n_item]))
		start += 1

	return np.array(movsum_result)

def concat(tb1, tb2):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return np.append(tb1, tb2)

def outputtofile(table, file):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	np.savetxt(file, table, delimiter = "|")

def Btree(table, index_col):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	globals()[index_col+"_index"] = BTree() # mydata_pricerange_btree = BTree() 
	

	col_list = table[index_col]

	group = list(set(col_list))
	for gp in group:
		value_list = [i for i, v in enumerate(col_list) if v == gp]
		eval(index_col+"_index" + ".insert(gp, value_list)")


def Hash(table, index_col):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	globals()[index_col+"_index"] = {}
	

	col_list = table[index_col]

	group = list(set(col_list))
	for gp in group:
		value_list = [i for i, v in enumerate(col_list) if v == gp]
		exec(index_col+"_index[gp] = value_list")
