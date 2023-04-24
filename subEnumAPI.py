import routes.utility as utility
import subprocess
import os
import sys
import uuid
from flask import make_response,jsonify
from zipfile import ZipFile
import Tools.merging_technologies as merging_technologies
import Tools.naabuParser
import Tools.parseHttpDomains as httpDomainParser
import utility
from __main__ import app


def initialize(domain):
	# filepath = os.path.join( os.getcwd(), "Websites/" ) 
	# dirname = domain.split(".")[0].lower()
	# filename =  dirname + ".txt"
	# httpDomainsFile=""
	# if not os.path.exists(filepath+dirname):
	# 	os.mkdir(filepath+dirname)
	# 	print(f"Created the directory {filepath+dirname}")
	# 	fileloc = filepath+dirname+"/"   #shows the directory
	# 	print(fileloc)
	# else:
	# 	fileloc = filepath+dirname+"/"
	# return(fileloc)

	# Create folder of a domain
	folderName = utility.getFolderNameFromDomain(domain)
	if os.path.isdir(os.path.join(app.config['cachePath'], folderName)):
		print("Folder Already Exists, skipping folder Generation")
	else:
		os.mkdir(os.path.join(app.config["cachePath"], folderName))
	
	return os.path.join(app.config["cachePath"], folderName)

"""
def checkVirtualHosts(): #check for proper automation
	#check for virtual hosts and specifically the output
	#/home/neel/hacking/virtual-host-discovery/
	command = "ruby scan.rb --ip=<IP_Addr> --host=<domain/subdomain> | grep '(' "
	VHosts = os.popen(command).read()
	print(VHosts)
"""

# def subfinder(domain):
# 	print("\n\nRunning Subfinder")
# 	print("---------------------")
# 	subFinderFile = os.path.join()
# 	command = "subfinder --silent -d "+ domain + " | anew " + fileloc + "subDomains.txt"       #--silent flag to only show the subdomains as the output
# 	subfinder = os.popen(command).read()            # simply append the to the previous output, no processing required 
# 	print(subfinder)


# def assetfinder(domain):
# 	print("\n\nRunning AssetFinder")
# 	print("-----------------------")
# 	command = "assetfinder " + domain + " | anew " + fileloc + "subDomains.txt"
# 	assetfinder = os.popen(command).read()          # simply append the to the previous output, no processing required
# 	print(assetfinder)


# now get the subdomains approved by the user
# and use those for further processing

#-----------------------------------------------------------------------------------

def findHttpDomains(fileloc,subDomainFileName):
	# global fileloc
	#print("in httpDomains")
	httpDomainsFile = fileloc + "httpDomains.txt"
	command = "cat " + fileloc + subDomainFileName + " | grep "+ domain +" | httprobe | anew " + httpDomainsFile
	print(command)
	os.popen(command).read()
	print("HttProbed and created the file :" , httpDomainsFile)
	return(httpDomainsFile)

#---------------------------------------------------------------------------------------



def findJSFiles(httpDomainsFileName,basePath):  #fileloc is the baseDir
	# global httpDomainsFile
	print("Searching for JS FIles")
	print("----------------------")
	httpDomainsFileLocation = os.path.join(basePath, httpDomainsFileName)
	# command = "cat "+ httpDomainsFile +" | subjs | anew " + basePath + "JSfiles.txt"  # => lists out all the JS files linked to the domains in the filename.txt
	command = f"cat {httpDomainsFileLocation} | subjs | anew {os.path.join(basePath, 'JSfiles.txt')}"
	JSFiles = os.popen(command).read()
	print("now you can search manually/via a program for the JS files listed in the "+basePath+"JSfiles.txt file")


def SecretFinder(basePath,filename):
	print("Running Secret Finder on JS Files")
	JSFilesLocation = os.path.join(basePath, filename)
	JSfiles = open(JSFilesLocation).read().split("\n")
	mainCommand = "python3 ./Tools/SecretFinder/SecretFinder.py -i '{}' -o cli >> '{}'"
	for url in JSfiles:
		if url != "" :
			command = mainCommand.format(url,os.path.join(basePath,"JSFinder.txt"))
			print(command)
			op = os.popen(command).read()

#---------------------------------------------------------------------------------------


# def checkSubTakeover(httpDomainsFileName,basePath): #subzy
# 	print("Checking Subdomain Takeover")
# 	print("---------------------------")
# 	httpDomainsFileLocation = os.path.join(basePath, httpDomainsFileName)
# 	# command = "subzy --targets " + httpDomainsFile + " > " + basePath + "/subDomainTakeover.txt"
# 	command = f"subzy --targets {httpDomainsFileLocation} > {os.path.join(basePath,'subDomainTakeover.txt')}"
# 	takeover = os.popen(command).read()
# 	print(takeover)

def checkSubTakeover(httpDomainsFileName,basePath): #subzy
	print("Checking Subdomain Takeover")
	print("---------------------------")
	httpDomainsFileLocation = os.path.join(basePath, httpDomainsFileName)
	# command = "subzy --targets " + httpDomainsFile + " > " + basePath + "/subDomainTakeover.txt"
	command = f"subzy run --targets {httpDomainsFileLocation} --output {os.path.join(basePath,'subDomainTakeover.json')}"
	takeover = os.popen(command).read()
	print(takeover)


#----------------------------------------------------------------------------------------


# def takeSS(httpDomainsFile,basePath):
# 	print("Taking SS of websites")
# 	print("---------------------")
# 	baseDir = os.getcwd()
# 	# print(baseDir)
# 	command = "python3 " + baseDir +"/tools/webscreenshot/webscreenshot.py -i " + httpDomainsFile + " -o " + basePath + "images/"
# 	#input(command)
# 	SS = os.popen(command).read()
	
#----------------------------------------------------------------------------------------

def naabu(subDomainsFileName,domain,basePath):
	print("Doing basic Port scan using Naabu")
	print("---------------------------------")
	subDomainFileLocation = os.path.join(basePath,subDomainsFileName)
	portScanFile = os.path.join(basePath, "portScan.txt")
	# file = open(subDomainFileLocation,"r")
	# for currDomain in file:
	# 	if domain not in currDomain:
	# 		continue
	# 	print("\n",currDomain)
	# 	currDomain = currDomain.strip("\n")
	# 	# command = "naabu -host " + currDomain + " >> " + portScanFile
	# 	# op = os.popen(command).read()
	# 	# command = "echo '-' >> " + portScanFile
	# 	# op = os.popen(command).read()
	# 	print("----------------------------------------------------")
	# file.close()
	command = f"naabu -l {subDomainFileLocation} > {portScanFile}"
	op = os.popen(command).read()


def parseNaabuOutput(basePath):
	print(os.listdir(os.path.join(basePath)))
	if not os.path.isfile(os.path.join(basePath,"portScan.txt")):
		print("[-] File Not Found for naabu parsing")
		return
	print("[+] Parsing Naabu Output")
	isOK, errorMsg = Tools.naabuParser.parseNaabu(basePath)
	if isOK:
		print("[+] Successfully Parsed Naabu Output")

#---------------------------------------------------------------------------------------

def waybackurls(domain,basePath):
	print("Running WayBackUrls")
	print("-------------------")
	waybackFile = os.path.join(basePath, "waybackurls.txt")
	# command = "printf " + domain + " | waybackurls > " + waybackFile
	command = f"printf '{domain}' | waybackurls > {waybackFile}"
	print(command)
	op = os.popen(command).read()


def filterWayback(basePath,filename):
	print("making filtered outputs of waybackURLS")
	command = "bash ./Tools/waybackFilter.sh '{}' '{}'".format(os.path.join(basePath,"./"),filename)
	print(command)
	op = os.popen(command).read()
#---------------------------------------------------------------------------------------


# def findSubdomains(domain):
# 	#have written to the file subDomains.txt
# 	subfinder(domain)
# 	assetfinder(domain)
# 	# return the contents of the file fileloc+"subDomains.txt"
# 	with open(fileloc+"subDomains.txt") as f:
# 		subdomains = f.read().split("\n")
	# return(subdomains)


# def detectWAF(httpDomainsFileName,basePath):
# 	print("detecting WAF using wafw00f")
# 	httpDomainsFileLocation = os.path.join(basePath,httpDomainsFileName)
# 	# command = "wafw00f -i '{}' -o '{}wafDetails.txt' ".format(httpDomainsFileLocation,basePath)
# 	# command = "wafw00f -i " + httpDomains + " -o " + basePath + "wafDetails.txt"
# 	command = f"wafw00f -i {httpDomainsFileLocation} -o {os.path.join(basePath, 'wafDetails.txt')}"
# 	print(command)
# 	op = os.popen(command).read()

def detectWAF(httpDomainsFileName,basePath):
	print("detecting WAF using wafw00f")
	httpDomainsFileLocation = os.path.join(basePath,httpDomainsFileName)
	# command = "wafw00f -i '{}' -o '{}wafDetails.txt' ".format(httpDomainsFileLocation,basePath)
	# command = "wafw00f -i " + httpDomains + " -o " + basePath + "wafDetails.txt"
	command = f"wafw00f -i {httpDomainsFileLocation} -f json -o {os.path.join(basePath, 'wafDetails.json')}"
	print(command)
	op = os.popen(command).read()

#-----------------------------------------------------------------------------------------------------


def detectTechnologies(httpDomainsFileName,basePath):
	#make a cURL request or run webanalyse tool on the domain one by one and store their output
	
	makeDir = os.popen("mkdir -p '{}'".format(os.path.join(basePath, "technologies/"))).read()
	cmd = "wappalyzer '{}' --pretty > '{}'"
	httpDomainsFileLocation = os.path.join(basePath,httpDomainsFileName)
	for httpDomain in open(httpDomainsFileLocation):
		httpDomain = httpDomain.strip("\n")
		command = cmd.format(
			httpDomain,
			os.path.join(basePath,
				"technologies", 
				utility.getFileNameFromUrl(httpDomain, extension=".json")
				)
			)
		print(command)
		op = os.popen(command).read()


def mergingTechnologies(basePath, folderName="technologies"):
	if not os.path.isdir(os.path.join(basePath,folderName)):
		print("[-] Invalid Path for merging technologies")
		return()
	print("[+] Merging Technologies ")
	Tools.merging_technologies.mergeTechnologies(os.path.join(basePath,folderName))

#-----------------------------------------------------------------------------------------------------

def takeSS(httpDomainsFile,basePath):
	os.mkdir(basePath+"images/")
	imgPath = basePath+"images/"
	oriCmd = "screenshoteer --url '{}' --file '{}{}.png' "
	with open(httpDomainsFile) as file:
		for line in file:
			url = line.strip("\n")
			cmd = oriCmd.format( url, imgPath, "_".join(url.split("/")) )
			op = os.popen(cmd).read()


#-----------------------------------------------------------------------------------------------------


#store the domains to be further processed in a file and pass that file path to findHttpDomains
def completeProcess(domain=None,options=None,subDomains=None,httpDomains=None):
	basePath = initialize(domain)
	if domain!=None:
		if "wayBackUrls" in options:
			waybackurls(domain,basePath)
			filterWayback(basePath,"waybackurls.txt")
		#perform GF-patterns on waybackURLS output

	if options != None:
		if subDomains != None:
			if len(subDomains) > 0:
				subDomainsFileName = "subDomains.txt"
				overwrite=False
				if "overwriteSubDomains" in options:
					overwrite=True
				createFile(subDomains,basePath,subDomainsFileName, overwrite=overwrite)
				if "portScan" in options:
					naabu(subDomainsFileName,domain,basePath)
					parseNaabuOutput(basePath)
	
		if httpDomains!=None:
			if len(httpDomains) > 0:
				httpDomainsFileName = "httpDomains.txt"
				overwrite=False
				if "overwriteHttpDomains" in options:
					overwrite=True
				createFile(httpDomains,basePath,httpDomainsFileName, overwrite=overwrite)  #returns the filename having only domains with http server running
				httpDomainParser.parseHttpDomainsFile(basePath)
				if "JSFiles" in options:
					findJSFiles(httpDomainsFileName,basePath)
					SecretFinder(basePath,"JSfiles.txt")
				if "subTakeover" in options:
					checkSubTakeover(httpDomainsFileName,basePath)
				if "wafDetect" in options:
					print("trying WAF detection")
					detectWAF(httpDomainsFileName,basePath)
				if "detectTechnology" in options:
					print("trying technology detection")
					detectTechnologies(httpDomainsFileName,basePath)
					mergingTechnologies(basePath)
				if "takeSS" in options:
					print("Taking Screnshots")
					takeSS(httpDomainsFileName,basePath)
	
	#now zip the particular folder and send it to the user
	# zipFolder(basePath,domain)



def getAllPaths(basePath):
	file_paths = []
  
	# crawling through directory and subdirectories
	for root, directories, files in os.walk(basePath):
		for filename in files:
			filepath = os.path.join(root, filename)
			file_paths.append(filepath)
  
	return file_paths


def zipFolder(basePath,domain):
	file_paths = getAllPaths(basePath)
	length = len(basePath)
	with ZipFile(os.path.join(app.config["cachePath"], utility.getFolderNameFromDomain(domain) + ".zip"),'w') as zip:
		# writing each file one by one
		for file in file_paths:
			filename = file[length:]
			zip.write(file,filename)


def createFile(listOfString,basePath,filename,overwrite=False):
	print("creating file",os.path.join(basePath,filename))
	if os.path.isfile(os.path.join(basePath,filename)):
		print("[INFO]: File already present")
		if not overwrite:
			print("[INFO]: using already present file")
			return
	file = open(os.path.join(basePath,filename),"w")
	file.write( utility.escapeOSCI("\n".join(listOfString),['\n']) )
	file.close()
	return()




def returnResponse(code, msg, data=""):
	if len(data)!=0:
		return( make_response( jsonify({ "code": code, "msg": msg, "data": data }), code ) )
	return( make_response( jsonify({ "code": code, "msg": msg }), code ) )	