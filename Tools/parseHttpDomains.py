from urllib.parse import urlparse
import json
import os

def parseHttpDomainsFile(inputFilePath, inputFileName="httpDomains.txt", outputFileName="parsedHttpDomains.json"):
	inputFile = os.path.join(inputFilePath, inputFileName)
	with open(inputFile) as file:
		httpDomains = file.read().split("\n")

	httpDomainDict = {}

	for httpDomain in httpDomains:
		try:
			x = urlparse(httpDomain)
			# print(httpDomain," => ", x.hostname)
			httpDomainDict.setdefault(x.hostname, [])
			httpDomainDict[x.hostname].append(httpDomain)
		except Exception as e:
			print("[ERROR]: parsing http domain file")

	httpDomainDict.pop(None,None)
	httpDomainDict.pop("",None)

	for i in httpDomainDict.keys():
		print(i, httpDomainDict[i])
	
	outputFile = os.path.join(inputFilePath, outputFileName)
	with open(outputFile,"w") as file:
		json.dump(httpDomainDict, file)


#for item in dirs:
#	if os.path.isdir(os.path.join(path,item)):
#		tldPath = os.path.join(path, item)
#		print(tldPath)
#		parseHttpDomains(tldPath)
