import requests
from inputimeout import inputimeout


resp = requests.get("http://localhost:5000/checkCName?companyName=avaya")
print(resp.json())

didNotPerformAttack=[]

for document in resp.json():
	print("==> ",document["tld"],document["isDataPresent"])
	# print()
	try:
		choice = inputimeout(prompt=" start.? ", timeout=5)
	except Exception:  
		print("no input, default choice taken ")
		choice="y"

	if not ( choice == "y" or choice == "Y" ):
		didNotPerformAttack.append(document["tld"])
		continue
	print("[INFO] finding Subdomains ")
	subData = {"domain": document["tld"]}
	resp = requests.post("http://localhost:5000/findSubDomains", json=subData)
	checked = resp.json()["checked"]

	print("[INFO]: finding httpDomains")
	httprobeData = {"domains": checked}
	resp = requests.post("http://localhost:5000/httprobe", json=httprobeData)
	urls = resp.json()["urls"]

	print("[INFO]: starting Attack")

	AttackData = {
		"domain": document["tld"],
		"httpDomains": urls,
		"options": [
			"wayBackUrls","portScan","JSFiles","subTakeover","wafDetect","detectTechnology"
		],
		"subDomains": checked
	}

	resp = requests.post("http://localhost:5000/Attack", json=AttackData)
	print("Attack Completed ",resp.json())
	print("** Skipped: ",didNotPerformAttack,"**")