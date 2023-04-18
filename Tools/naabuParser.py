import json
import os

# filename = "/home/yash/hacking/portScanCelo.txt"
#filePath = "/home/yash/hacking/"
#fName = "portScanCelo.txt"
#filename = filePath+fName


#isOK,errMsg
def parseNaabu(filePath,filename="portScan.txt"):
	mainJson={}
	if not os.path.isfile(os.path.join(filePath,filename)):
		print("File Not Found")
		return(False, "Input File Not Found")

	with open(os.path.join(filePath,filename)) as file:
		for line in file:
			parts=line.strip("\n").split(":")
			try:
				subDomain, port = parts
				if subDomain in mainJson:
					mainJson[subDomain].append(int(port))
				else:
					mainJson[subDomain] = [int(port)]
			except Exception as error:
				# print("Error => ",error)
				# print(line)
				pass

	# for i in mainJson.keys():
	# 	print(i,mainJson[i])

	l = [ [i,mainJson[i],len(mainJson[i])] for i in mainJson ]


	l.sort(key=lambda x:x[2], reverse=True)
	# for i in l:
	# 	print(i)
	# print(len(l))

	mainJson = {item[0]:[item[1],item[2]] for item in l}
	for i in mainJson.keys():
		print(i,mainJson[i])


	with open(os.path.join(filePath,"parsedNaabu.json"),"w") as file:
		json.dump(mainJson,file)
	return(True, "")


#parseNaabu("/home/yash/Desktop/GLIDE/sampleData/", "portScanCelo.txt")
