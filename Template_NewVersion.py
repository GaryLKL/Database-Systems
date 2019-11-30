def inputfromfile(file_path):
	'''
	1. Function: to read the data into "mydata" line by line
	2. Inputs: the path of the text file whose delimiter is "|" and headers are in the first line
	3. Outputs: a n*m array data
	4. Side Effect: 
	'''
	global headers

	with open(file_path) as file:
		for line in file:
			self.mydata.append(line.split("|"))
	
	headers = dict(zip(mydata[0], range(len(mydata[0]))))
	
	return mydata[1:]

def select(table, statemt):
	'''
	1. Function: to select all columns from the table with restricted rows under the statement
	2. Inputs: "table" means a 2-dimension array data; "statemt" is the string-type condition statement
	3. Outputs: a n*m array data
	4. Side Effect:
	'''

	if "and" in statemt:
		conditions = statemt.split("and")



	return 

def project(table, *args):
	'''
	1. Function: 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return 

def avg():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''


	return

def sum():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def count():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def countgroup():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return 
	
def sumgroup():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return


def avggroup():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def join():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def sort():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def movavg():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def movsum():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def concat():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return

def outputtofile():
	'''
	1. Function: to select all columns 
	2. Inputs: 
	3. Outputs:
	4. Side Effect:
	'''

	return 

