# from ..server import app
from __main__ import app
from flask import jsonify,request
from .utility import *
import utility as mainUtility

@app.route("/findSubDomains",methods=['GET','POST'])
def findSubDomains():
	if request.method == "GET":
		return("OK")
	# domain = "vupune.ac.in"
	if not request.json:
		return(utility.Response(code=400, msg="No data sent"))
	domain = request.json.get("domain")
	if domain == None:
		return(utility.Response(code=400, msg="Domain not specified"))
	print("received subdomains request for ",domain)
	#do error checking
	subdomains = []
	subdomains.extend(subfinder(domain))
	subdomains.extend(assetfinder(domain))
	# print(subdomains)
	subdomains.append(domain)
	subdomains = list(set(subdomains))
	checked,unchecked = findRelevantSubdomains(subdomains,domain)
	print("Subdomains : checked : ",checked,"\nUnchecked : ",unchecked)
	return(jsonify({ "checked":checked , "unchecked": unchecked}))
