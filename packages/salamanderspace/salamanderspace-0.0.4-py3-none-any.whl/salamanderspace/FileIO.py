"""
TODO:

Documentation at top of modules
Write read/split functions for floats,int, "strings" (mixed)
		Test bc csvs are weird
		Code other delimiters
Create list of functions (aka plan out packages)
"""


def readFile(name):
	"""
	This function will read the contents of a file by a given name in the "Files" folder of this function
	Input: String name = the name of the file to be read with file extension
	Output: array lines = array of each of the lines
	"""

	# get the path of the input file relative to this file
	import os
	#get teh current path and the current script name
	curPath = os.path.abspath(__file__)
	scriptName = os.path.basename(__file__)

	#change the slashes
	curPath = curPath.replace("\\","//")
	#change path to be towards the file to read
	curPath = curPath.replace(scriptName,"Files//"+name)

	#open the file
	f = open(curPath,"r")
	#read the file
	lines = f.readlines()
	#close the file
	f.close()
	
	#returns unclean array of each of the lines
	return lines


def splitCSV(lines):
	"""
	This function will take in an array from a csv file and split it into 'cells'
	input: array lines = an array of data delimited by a comma and each line ends with a \n
	output: 2d array data = array of arrays that is the data of each 'cell'
	"""

	#initialize the return array data
	data = []
	
	#create the 2d data array of clean data
	for i in range(0,len(lines)):
		data.append(lines[i].strip("\n").split(","))

	#return the proper array
	return data


def filetoarray(file,**kwargs):
	"""
	filetoarray will return 2d array from file
	Inputs:
		string file = path of file to seperate
		**kwars:
			tuple(int) bounds = tuple of ints with bounds (default 0,n)
			string delim = delimiter to split each line (default ",")
			string dataType = type of data to change cells into. (default string))
				Options:
					string = string,str,s
					int = int, i
					complex = complex, com, c
					float = float, f
			
	"""
	
	#Open reader
	f = open(file,"r")


	##Setting reading options
	if kwargs["dataType"] is not None:
		dataType = kwargs["dataType"]
	else:
		dataType = "s"

	if kwargs["delim"] is not None:
		delim = kwargs["delim"]
	else:
		delim = ","
	

	#reading file
	lines = f.readlines()
	
	data = []
	for i in range(kwargs["bounds"][0],kwargs["bounds"][0]):
		splitline =lines[i].strip("\n").split(delim)
		templine = []

		##Change element type
		for j in range(len(splitline)):
			try:
				if dataType.lower() == "s" or dataType.lower() == "str" or dataType.lower() == "string":
					templine.append(str(splitline[j]))
				elif dataType.lower() == "f" or dataType.lower() =="float":
					templine.append(float(splitline[j]))
				elif dataType.lower() == "i" or dataType.lower() == "int":
					templine.append(int(splitline[j]))
				elif dataType.lower() =="c" or dataType.lower() == "com" or dataType.lower() == "complex":
					templine.append(complex(splitline[j]))
				else:
					print("ERROR:dataType not recognized")
			except:
				templine.append(splitline[j])

		#append to master file
		data.append(templine)

	return data


def timer(toTest,correct=None,**kwargs):
    from datetime import datetime
    result = None
    #Start Timer
    start = datetime.now()

    
    result = toTest(**kwargs)


    #Stop Timer
    finish = datetime.now()
    #get elapsed time
    elapse = finish-start


    print("\tTest Finished")
    print("=====================================")
    print("Time Elapsed:\t",elapse," sec")
    print("Given Result:\t",result)
    print("Correct Result:\t", correct)