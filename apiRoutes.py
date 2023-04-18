from __main__ import app
import os, json
from flask import Flask,request,jsonify
import utility

@app.route("/checkCName",methods=["GET"])
def checkCompanyName():
	companyName = request.args.get("companyName")
	if companyName == None:
		return utility.Response(code=400 , msg="Company Name not provided")
	if not str(companyName).isalpha():
		return utility.Response(code=400 , msg="CompanyName should be strictly str type")
	fileName = str(companyName)+"Domains.txt"
	if fileName in os.listdir(app.config["cachePath"]):
		print("Set = ",set(open(os.path.join(app.config["cachePath"], fileName)).read().split("\n")).remove(""))
		# setOfDomains = open(os.path.join(app.config["cachePath"], fileName)).read().split("\n")
		with open(os.path.join(app.config["cachePath"], fileName)) as file:
			domains = file.read().split("\n")
		setOfDomains = set(domains)
		setOfDomains.remove("")
		listOfDomains = list(setOfDomains)
		cNameDetails = utility.getTldBasedData(listOfDomains)
		return utility.Response (code=200, 
			additionalPayloadData= {"data": jsonify(cNameDetails)}
			)
	return utility.Response(code=404, msg="File Not Found")
	


@app.route("/checkTLD", methods=["GET"])
def checkTldPresence():
	tldValue = request.args.get("tld")
	if tld == None:
		return utility.Response(code=400 , msg="tld not provided")


#return ports data for all subdomains for a given tld
@app.route("/ports", methods=['GET'])
def getPortsRoute():
	tld=request.args.get("tld")
	
	if not tld:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")
	# return("Folder Found")
	
	if "parsedNaabu.json" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("parsedNaabu File Found")
		try:
			with open(os.path.join(app.config["cachePath"], folderName, "parsedNaabu.json")) as file:
				tldJson = json.load(file)
		except Exception as e:
			print("[ERROR]: loading parsedNaabu file for tld ",tld, "with error ",e)
			return utility.Response(code=502, msg="error loading ports data")	
	# tldJson = folder.open(tld)
	else:
		return utility.Response(code=404, msg="Port scan details not found, kindly perform action for the given tld")

	# if subDomain not in tldJson:
	# 	print("[ERROR] Subdomain Data not found in TLD JSON")
	return utility.Response(code=200, msg="", additionalPayloadData={"data":tldJson, "length": len(tldJson)})
	# return tldJson[subdomain]


@app.route("/subDomain", methods=['GET'])
def getSubdomainData():
	tld=request.args.get("tld")
	
	if not tld:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")
	
	if "subDomains.txt" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("sub Domain File Found")
		try:
			with open(os.path.join(app.config["cachePath"], folderName, "subDomains.txt")) as file:
				subdomains = file.read().split("\n")
		except Exception as e:
			print("[ERROR]: loading subdomains file for tld ",tld, "with error ",e)
			return utility.Response(code=502, msg="error loading subdomains data")
	else:
		return utility.Response(code=404, msg="Subdomain details not found, kindly perform action for the given tld")

		while "" in subdomains:
			print("removing Empty Quote")
			subdomains.remove('')

		return utility.Response(code=200, additionalPayloadData={"data": subdomains, "length": len(subdomains)})


@app.route("/httpDomains", methods=["GET"])
def getHttpDomainsJsonData():
	tld=request.args.get("tld")
	if not tld:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")

	if "parsedHttpDomains.json" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("parsedHttpDomains File Found")
		try:
			with open(os.path.join(app.config["cachePath"], folderName, "parsedHttpDomains.json")) as file:
				tldJson = json.load(file)
		except Exception as e:
			print("[ERROR]: loading parsedHttpDomains file for tld ",tld, "with error ",e)
			return utility.Response(code=502, msg="error loading httpDomains data")	
	else:
		return utility.Response(code=404, msg="Http Domain details not found, kindly perform action for the given tld")
	
	return utility.Response(code=200, msg="", additionalPayloadData={"data":tldJson, "length": len(tldJson)})



@app.route("/subDomainTakeoverData", methods=["GET"])
def getSubDomainTakeoverData():
	tld=request.args.get("tld")
	if not tld:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")

	if "subDomainTakeover.json" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("subdomain Takeover Data File Found")
		try:
			with open(os.path.join(app.config["cachePath"], folderName, "subDomainTakeover.json")) as file:
				tldJson = json.load(file)
		except Exception as e:
			print("[ERROR]: Loading SubDomain Takeover file for tld ",tld, "with error ",e)
			return utility.Response(code=502, msg="error loading subdomain Takeover data")	
	else:
		return utility.Response(code=404, msg="Subdomain takeover details not found, kindly perform action for the given tld")
	for item in tldJson:
		item.pop("discussion",None)
		item.pop("documentation",None)
		item.pop("engine",None)

	return utility.Response(code=200, msg="", additionalPayloadData={"data":tldJson, "length": len(tldJson)})



@app.route("/getWafDetails", methods=["GET"])
def getWafDetails():
	tld=request.args.get("tld")
	if not tld:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")

	if "wafDetails.json" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("waf Details Data File Found")
		try:
			with open(os.path.join(app.config["cachePath"], folderName, "wafDetails.json")) as file:
				tldJson = json.load(file)
		except Exception as e:
			print("[ERROR]: Loading waf Details file for tld ",tld, "with error ",e)
			return utility.Response(code=502, msg="error loading waf Details data")	
	else:
		return utility.Response(code=404, msg="Web Application Firewall details details not found, kindly perform action for the given tld")

	for item in tldJson:
		item.pop("manufacturer",None)

	return utility.Response(code=200, msg="", additionalPayloadData={"data":tldJson, "length": len(tldJson)})

@app.route("/getWebTech", methods=["GET"])
def getWebTechGetRoute():
	tld=request.args.get("tld")
	subdomain = request.args.get("subdomain")
	if not tld or not subdomain:
		print("[ERROR] TLD + SubDomain Combo not provided")
		return utility.Response(code=400 , msg="[ERROR] TLD + SubDomain Combo not provided")
	
	# if tld not in folder:
	# 	print("[ERROR] TLD Data Not Found")
	folderName = utility.getFolderNameFromDomain(tld)
	if folderName not in os.listdir(app.config['cachePath']):
		return utility.Response(code=404 , msg="Top Level Domain Data Not Found")
	
	if "technologies" in os.listdir(os.path.join(app.config["cachePath"], folderName)):
		print("Found Technology folder found")
		technologyPath = os.path.join(app.config["cachePath"], folderName, "technologies")

		technologyFiles = os.listdir(technologyPath)
		# print('technologyFiles ',technologyFiles)
		
		technologyDetails = {}
		webServerUrl = f"http://{subdomain}"
		filename = utility.getFileNameFromUrl(webServerUrl) + ".json"

		if filename in technologyFiles:
			try:
				with open(os.path.join(technologyPath, filename)) as file:
					techFile = json.load(file)
					print(techFile.keys())
					technologyDetails[webServerUrl] = techFile["technologies"]
			except Exception as e:
				print("error opening web Tech File")
				return utility.Response(code=502, msg="couldnt fetch Web Technology details")
			
		
		webServerUrl = f"https://{subdomain}"
		filename = utility.getFileNameFromUrl(webServerUrl) + ".json"

		if filename in technologyFiles:
			try:
				with open(os.path.join(technologyPath, filename)) as file:
					techFile = json.load(file)
					print(techFile.keys())
					technologyDetails[webServerUrl] = techFile["technologies"]
			except Exception as e:
				print("error opening web Tech File")
				return utility.Response(code=502, msg="couldnt fetch Web Technology details")

	else:
		return utility.Response(code=404, msg="Web Technology details not found, kindly perform action for the given tld")

	return utility.Response(code=200, msg="", additionalPayloadData={"data": technologyDetails})