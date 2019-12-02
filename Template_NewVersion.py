import numpy as np
import re
from itertools import product
# The following packages are for BTree
import ZODB 
from BTrees.OOBTree import BTree


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

		delim = re.findall("=|<|>|!=|<=|>=", condition)[0] # e.g. ">"
		
		latter = condition.split(delim)[1].strip(" +")

		delim_latter = delim + " '" + latter + "'"
		# Change the type of the column from string to int
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
				remain_index = []
				unique_keys = eval("list("+column_name+"_index.keys())")
				keys_under_condition = eval("[i for i in unique_keys if i"+delim_latter+"]")
				for i in keys_under_condition:
					remain_index = remain_index + eval(column_name+"_index.get(i)")
				return remain_index

			else:
				#eval("[i for i, v in enumerate(mytable['time'] > 40) if v == True]")
				remain_index = "[i for i, v in enumerate(table[column_name]" + delim_latter + ") if v == True]"
				return eval(remain_index) # the index of the true condition
		except:
			print("Some errors may happen in your btree or hash format.")


	table_type = table.dtype
	if " and " in statemt or ")and " in statemt or " and(" in statemt or ")and(" in statemt:
		delim = re.findall(" and |\)and | and\(|\)and\(", statemt)[0]
		conditions = statemt.split(delim)
		for con in conditions:
			table = [table[i] for i in get_remain_index(con, table)]


	elif " or " in statemt or ")or " in statemt or " or(" in statemt or ")or(" in statemt:
		remain_index_or_condition = []
		delim = re.findall(" or |\)or | or\(|\)or\(", statemt)[0]
		conditions = statemt.split(delim)
		for con in conditions:
			remain_index_or_condition = remain_index_or_condition + get_remain_index(con, table) # e.g. [] + [1,2] + [2,3,4] -> [1,2,2,3,4]

		final_or_index = set(remain_index_or_condition) # e.g. [1,2,2,3,4] -> [1,2,3,4]

		table = [table[i] for i in final_or_index]

	else:
		# only one condition
		table = [table[i] for i in get_remain_index(statemt, table)]

	# give the column name and data type to the array

	return np.array(table, dtype = table_type)


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

		tb1_col = re.split("=|<|>|!=|<=|>=", condition)[0].strip(" +").split(".")[1] # "qty"
		tb2_col = re.split("=|<|>|!=|<=|>=", condition)[1].strip(" +").split(".")[1] # "Q"

		mydelimiter = re.findall('=|<|>|!=|<=|>=', condition)[0] # ">"
		
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

		index_dict = {} # {"tb1_index": "tb2_index_list"}
		if mydelimiter == "=":
			mydelimiter = "=="
			if tb1_col+"_index" in globals() and tb2_col+"_index" in globals():
				unique_keys_1 = eval("list("+tb1_col+"_index.keys())") # [1,2,3]
				unique_keys_2 = eval("list("+tb2_col+"_index.keys())") # [2,3,4]
				same_keys = list(set(unique_keys_1) & set(unique_keys_2)) # [2,3]

				for k in same_keys:
					for i in eval(tb1_col+"_index.get(k)"):
						index_dict[i] = eval(tb2_col+"_index.get(k)")

			elif tb1_col+"_index" in globals() and not tb2_col+"_index" in globals():
				unique_keys_1 = eval("list("+tb1_col+"_index.keys())")
				unique_keys_2 = list(set(tb2[tb2_col]))
				same_keys = list(set(unique_keys_1) & set(unique_keys_2))

				for k in same_keys:
					for i in eval(tb1_col+"_index.get(k)"):
						index_dict[i] = [ind for ind, val in enumerate(tb2[tb2_col]) if val == k]

			elif not tb1_col+"_index" in globals() and tb2_col+"_index" in globals():
				unique_keys_1 = list(set(tb1[tb1_col]))
				unique_keys_2 = eval("list("+tb2_col+"_index.keys())")
				same_keys = list(set(unique_keys_1) & set(unique_keys_2))

				for k in same_keys:
					tb1_match_ind = [ind for ind, val in enumerate(tb1[tb1_col]) if val == k]
					for i in tb1_match_ind:
						index_dict[i] = eval(tb2_col+"_index.get(k)")

			else:
				# without any index 
				for indexone in range(len(tb1)):
					index_dict[indexone] = []
					for indextwo in range(len(tb2)):
						#eval("if tb1["+str(indexone)+"]["+str(col_index_1)+"] "+mydelimiter+" tb2["+str(indextwo)+"]["+str(col_index_2)+"]: "+"index_dict["+str(indexone)+"].append("+str(indextwo)+")")
						result_bool = eval("tb1[tb1_col][indexone] " + mydelimiter + " tb2[tb2_col][indextwo]")
						if result_bool == True:
							index_dict[indexone].append(indextwo)

		else:
			# the comparison symbol is not "="
			for indexone in range(len(tb1)):
				index_dict[indexone] = []
				for indextwo in range(len(tb2)):
					#eval("if tb1["+str(indexone)+"]["+str(col_index_1)+"] "+mydelimiter+" tb2["+str(indextwo)+"]["+str(col_index_2)+"]: "+"index_dict["+str(indexone)+"].append("+str(indextwo)+")")
					result_bool = eval("tb1[tb1_col][indexone] " + mydelimiter + " tb2[tb2_col][indextwo]")
					if result_bool == True:
						index_dict[indexone].append(indextwo)


		# Add the column

		return index_dict


	final_table = []
	if " and " in by_condition or ")and " in by_condition or " and(" in by_condition or ")and(" in by_condition:
		delim = re.findall(" and |\)and | and\(|\)and\(", by_condition)[0]
		dict_list = []
		conditions = by_condition.split(delim)

		# get the two tables name
		condition_for_table_name = conditions[0].strip("(\(|\)| )+")
		table_one_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[0].strip(" +").split(".")[0]
		table_tw0_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

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
		table_tw0_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

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
		table_tw0_name = re.split("=|<|>|!=|<=|>=", condition_for_table_name)[1].strip(" +").split(".")[0]

		# start
		index_table = get_index(by_condition, tb1, tb2)
		for ind_1, ind_2 in index_table.items():
			if len(ind_2) > 0:
				for each_ind_2 in ind_2:
					final_table.append(tuple(list(tb1[ind_1]) + list(tb2[each_ind_2])))

	# give column name and data type to the array
	table_one_col_name = [table_one_name + "_" + i for i in tb1.dtype.names]
	table_two_col_name = [table_two_name + "_" + i for i in tb2.dtype.names]
	full_table_col_name = tuple(table_one_col_name + table_two_col_name)

	formats = ["<U10"] * len(full_table_col_name)
	datatype = np.dtype({'names': full_table_col_name, 'formats': formats})

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
