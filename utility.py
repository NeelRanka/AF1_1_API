from flask import jsonify,request, make_response

def getFolderNameFromDomain(domain):
	folderName = domain.replace(".","_").replace("/","_").replace(":","_")
	return folderName

def getFileNameFromUrl(url, extension = None):
	fileName = url.replace("/","_")#.replace(".","_").replace(":","_")
	if extension:
		fileName = fileName+extension
	return fileName


def getTldBasedData(tldList):
	cachedFolders = os.listdir(app.config["cachePath"])
	document = []
	for tld in tldList:
		if utility.getFolderNameFromDomain(tld) in cachedFolders:
			document.append(
				{
					"tld": tld,
					"isDataPresent": True
				}
			)
		else:
			document.append(
				{
					"tld": tld,
					"isDataPresent": False
				}
			)
	return(document)


OSallowed = {
			'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1,
			'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1,
			'k': 1, 'l': 1, 'm': 1, 'n': 1, 'o': 1, 'p': 1, 'q': 1, 'r': 1, 's': 1, 't': 1,
			'u': 1, 'v': 1, 'w': 1, 'x': 1, 'y': 1, 'z': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 1,
			'E': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1, 'J': 1, 'K': 1, 'L': 1, 'M': 1, 'N': 1,
			'O': 1, 'P': 1, 'Q': 1, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 1, 'W': 1, 'X': 1,
			'Y': 1, 'Z': 1, '-': 1, '.': 1, '_': 1, ':': 1, "/": 1
			}


def escapeOSCI(string,extraAllowed=[]):
	print("in escapeOSCI")
	string = string.encode().decode("unicode-escape")
	# print(string)
	string = list(string)
	index=0
	length = len(string)
	lastStart = None
	newStr = []
	for char in string:
		if char not in extraAllowed:
			if char not in OSallowed:
				# newStr.append("\\")
				continue
		newStr.append(char)
	string = "".join(newStr)
	# print(string)
	return(string)


def Response(code, msg="", additionalPayloadData={}):
	respPayload = { "code": code }
	if msg != "":
		respPayload.update({"msg":msg})
	respPayload.update(additionalPayloadData)
	return make_response( jsonify(respPayload), code )