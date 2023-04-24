import os
import json

# location = "/home/neel/hacking/Websites/vupuneReconZip/technologies"
def mergeTechnologies(location):
	files = os.listdir(location)
	if "combined.json" in files:
		print("[INFO]: Deleting Combined JSON")
		os.remove(os.path.join(location, "combined.json"))
		files.remove("combined.json")
	#print(files)
	finalJsonDict = {}
	for eachFile in files:
		with open(os.path.join(location,eachFile)) as file:
			# print(file)
			data={}
			try:
				data = json.load(file)
			except Exception as e:
				print("[-] Could Not decode JSON file ",e)
				data = {}
				
			#print("KEYS => ",data.keys())
			# loop over technologies
			if "technologies" in data:
				for technology in data["technologies"]:
					#print(technology)
					techName = technology["name"]
					if techName not in finalJsonDict:  #new Technology found
						# name as key and dict of version objects as value
						finalJsonDict[techName] = {}
						version = "Version=" + str(technology["version"])
						if version not in finalJsonDict[techName]:
							finalJsonDict[techName][version] = [eachFile]
						else:
							finalJsonDict[techName][version].append(eachFile)
					else:  #technology already present
						version = "Version=" + str(technology["version"])
						if version not in finalJsonDict[techName]:
							finalJsonDict[techName][version] = [eachFile]
						else:
							finalJsonDict[techName][version].append(eachFile)
			else:
				print("[-] Technologies part not found in JSON ", eachFile)
		


	with open(os.path.join(location,"combined.json"), "w") as outputFile:
		json.dump(finalJsonDict,outputFile)


#mergeTechnologies("/home/yash/Desktop/GLIDE/sampleData/technologies")
