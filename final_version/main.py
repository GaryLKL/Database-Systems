from functions import *
import time

command_file_path = "command.txt"
if __name__ == "__main__":

	commands = []

	#open two text files to save the result and time:
	timefile = open("processing_time.txt", "w")
	
	resultfile = open("alloperations.txt", "w")

	# Read the command file
	with open(command_file_path, "r") as file:
		for line in file:
			commands.append(line.strip("\n"))

	# Start the command function
	for func in commands:
		start = time.time()
		try:
			func_name = func.split(":=")[1].split("(")[0].strip(" ") # e.g. inputfromfile
		except:
			func_name = func.split("(")[0].strip(" ")
			
		# determine which function to use
		if func_name == "inputfromfile":
			path = func.split("(")[1].strip("( |\))").strip(" ") # e.g. "test.txt" 
			assigned_name = func.split(":=")[0].strip(" ") # e.g. R
			exec(assigned_name+"="+func_name+"('"+path+"')") # e.g. R = inputfromfile('test.txt') -> exec("R = inputfromfile('test.txt')")

		if func_name == "select":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ")  # ex. "R"
			arg = func.split(",")[1].strip(" ")[:-1]  # ex. (time > 50) or (qty < 30))
			assigned_name = func.split(":=")[0].strip(" ") # ex. R1
			exec(assigned_name+"="+func_name+"("+table+","+  "'"+ arg+"'" + ")") # e.g. R1 := select(R, (time > 50) or (qty < 30)) -> exec("R1 = select(R, 'time >50 or qty <30')")
			
		if func_name == "project":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ")  # ex. "R1"
			col = func.split("(")[1].strip("( |\))").split(",")[1:]
			col = [i.strip(" +") for i in col]  # ' saleid', ' qty', ' pricerange'
			assigned_name = func.split(":=")[0].strip(" ") # ex. R2
			exec(assigned_name+"="+func_name+"("+table+","+  str(col).strip("[]") + ")") 
			
		if func_name == "avg":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ") # ex. "R1"
			col =  func.split("(")[1].strip("( |\))").split(",")[1].strip(" ")  # qty
			assigned_name = func.split(":=")[0].strip(" ")  # R3
			exec(assigned_name+"="+func_name+"("+table+","+"'"+ col +"'"+ ")") 
		
		#R4 := sumgroup(R1, time, qty)   
		if func_name == "sumgroup":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ") # ex. "R1"
			col =  func.split("(")[1].strip("( |\))").split(",")[1:]  # qty
			col = [i.strip(" +") for i in col]
			assigned_name = func.split(":=")[0].strip(" ")  # R3
			exec(assigned_name+"="+func_name+"("+table+","+  str(col).strip("[]") + ")") 
		#R6 := avggroup(R1, qty, pricerange)
		if func_name == "avggroup":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ") # ex. "R1"
			col =  func.split("(")[1].strip("( |\))").split(",")[1:]  # qty, pricerange
			col = [i.strip(" +") for i in col]
			assigned_name = func.split(":=")[0].strip(" ")  # R6
			exec(assigned_name+"="+func_name+"("+table+","+  str(col).strip("[]") + ")") 
		# T := join(R, S, R.customerid = S.C)
		if func_name == "join":
			table = func.split("(")[1].strip("( |\))").split(",")[0:2]# ex. "R, S"
			table = [i.strip(" +") for i in table]
			col =  func.split(",")[2][:-1].strip(" ") # R.customerid = S.C
			assigned_name = func.split(":=")[0].strip(" ")  # R3
			exec(assigned_name+"="+func_name+"("+str(table).strip("[]").replace("'", "")+", '"+ col + "')") 
		#T1 := join(R1, S, (R1.qty > S.Q) and (R1.saleid = S.saleid))



		# 'T2 := sort(T1, S_C)'
		if func_name == "sort":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ")# ex. "T1"
			col =  func.split("(")[1].strip("( |\))").split(",")[1:]  # S_C
			col = [i.strip(" ") for i in col]
			assigned_name = func.split(":=")[0].strip(" ")  # T2
			exec(assigned_name+"="+func_name+"("+table+","+  str(col).strip("[]") + ")")

		#T3 := movavg(T2prime, R1_qty, 3)
		if func_name =='movavg':
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ")
			col =  func.split("(")[1].strip("( |\))").split(",")[1].strip(" ")
			nitem = func.split("(")[1].strip("( |\))").split(",")[2].strip(" ")
			assigned_name = func.split(":=")[0].strip(" ")
			exec(assigned_name+"="+func_name+"("+table+", "+ "'" + col + "', " + nitem + ")")

		if func_name =='movsum':
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ")
			col =  func.split("(")[1].strip("( |\))").split(",")[1].strip(" ")
			nitem = func.split("(")[1].strip("( |\))").split(",")[2].strip(" ")
			assigned_name = func.split(":=")[0].strip(" ")
			exec(assigned_name+"="+func_name+"("+table+", "+ "'" + col + "', " + nitem + ")")

		#Btree(R, qty)
		if func_name == "Btree":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ") # ex. "R1"
			col =  func.split("(")[1].strip("( |\))").split(",")[1].strip(" ")  # qty
			exec(func_name+"("+table+","+"'"+ col +"'"+ ")") 

		#Q5 := concat(Q4, Q2). concat 要改一下程式，讓他可以讀 concat(R, R1) 
		if func_name == "concat":
			table = func.split("(")[1].strip("( |\))").strip(" ")# ex. "Q4, Q2"
			assigned_name = func.split(":=")[0].strip(" ") 
			exec(assigned_name+"="+func_name+"("+table +")")

		# outputfromfile(Q5, Q5)
		if func_name == "outputtofile":
			table = func.split("(")[1].strip("( |\))").split(",")[0].strip(" ") # ex. "Q5"
			col =  func.split("(")[1].strip("( |\))").split(",")[1].strip(" ")  # Q5
			exec(func_name+"("+table+","+"'"+ col +"'"+ ")")

		end = time.time()
		processingTime = 'Processing time for "%s" is: %s sec.' % (func, str(round(end - start, 3)))
		print(processingTime)

		# save
		timefile.write(processingTime + "\n\n")


		try:
			outdata = eval(assigned_name)
			result = '|'.join(outdata.dtype.names) + '\n' + ''.join(['|'.join(i) + '\n' for i in outdata])
		except:
			pass
		resultfile.write("The result of '%s' is:\n" % func + result + "\n\n\n")
	timefile.close()
	resultfile.close()



