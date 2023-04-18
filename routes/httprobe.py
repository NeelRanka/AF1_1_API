from __main__ import app
# from ..server import app
from flask import jsonify,request
from .utility import *


@app.route("/httprobe",methods=["GET","POST"])
def httprobeRoute():
	#do error checking
	# domain = ["vupune.ac.in"]
	domain = request.json['domains']
	result = httprobe(domain)
	results = list(set(result))
	print("httprobe : ",result)
	return(jsonify({"urls":result}))