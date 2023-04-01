import os
import json

# location = "/home/neel/hacking/Websites/vupuneReconZip/technologies"
def mergeTechnologies(location):
	files = os.listdir(location)
	print(files)
	finalJsonDict = {}
	for eachFile in files:
		with open(os.path.join(location,eachFile)) as file:
			print(file)
			data = json.load(file)
			print(data.keys())
			# loop over technologies
			for technology in data["technologies"]:
				print(technology)
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
		


	with open(os.path.join(location,"combined.json"), "w") as outputFile:
		json.dump(finalJsonDict,outputFile)


mergeTechnologies("/home/yash/Downloads/vupune/technologies")