from flask import Flask,request,jsonify,render_template
import os


app = Flask(__name__)

app.config["cachePath"] = os.path.join( os.getcwd(),"Websites")

if not os.path.isdir(app.config["cachePath"]):
	os.path.mkdir(app.config["cachePath"])

import routes 
from subEnumAPI import *
import apiRoutes

@app.route("/", methods=['GET'])
def landing():
	print("remote IP addr : ",request.remote_addr,request.origin,request.referrer)
	return("<h1>check '/Attack' page for Info Gathering<br>check '/results' page for results of those atacks<br></h1>")


@app.route("/new/",methods=["GET"])
def newPage():
	print("ARGS : ",dict(request.args))
	par = dict(request.args)
	return(par['x'])
	return("OK")


@app.route("/links",methods=["GET","POST"])
def links():
	print("in links")
	checked=[
	"vupune.ac.in",
	"erp.vupune.ac.in",
	"google.com"
	]
	unchecked=['neel.com']
	print(request.form)
	print(request.json)
	return(jsonify({"checked":checked,"unchecked":unchecked}))



@app.route("/Attack",methods=['GET'])
def HTML():
	return( render_template("indexMain.html") )


@app.route("/Attack",methods=["POST"])
def Attack():
	domain,subDomains,httpDomains,options = None,None,None,None
	print("in Attack")
	if request.json:
		print(request.json)
		if "domain" in request.json:
			domain = request.json["domain"]
		if "subDomains" in request.json:
			subDomains = request.json["subDomains"]
		if "httpDomains" in request.json:
			httpDomains = request.json["httpDomains"]
		if "options" in request.json:
			options = request.json["options"]
			print(options)

	if domain:
		completeProcess(domain,options,subDomains,httpDomains)
		return( returnResponse(code=200, msg="OK",data=domain) )
	else:
		return( returnResponse(code=400, msg="no domain provided") )


if __name__ == "__main__":
	app.run(debug=True,port=5000,host="0.0.0.0")
