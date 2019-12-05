from functions import *

command_file_path = input("Please input your command file here: ")
if __name__ == "__main__":

	commands = []
	# Read the command file
	with open(command_file_path, "r") as file:
		for line in file:
			commands.append(line.strip("\n"))

	# Start the command function
	for func in commands:
		func_name = func.split(":=")[1].split("(")[0].strip(" +") # e.g. inputfromfile

		# determine which function to use
		if func_name == "inputfromfile":
			path = func.split("(")[1].strip("( |\))") # e.g. "test.txt"
			assigned_name = func.split(":=")[0].strip(" +") # e.g. R
			exec(assigned_name+"="+func_name+"('"+path+"')") # e.g. R = inputfromfile('test.txt') -> exec("R = inputfromfile('test.txt')")
