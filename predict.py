import sys
import os
import graphlab as gl
from swift_wrapper import upload_from_file, download
import zipfile
import json

def predict(modelname, userList):
	resultList = {}
	if os.path.exists(modelname):
		model = gl.load_model(modelname)
		recommendedItemList = model.recommend(users=userList)
		for user in userList:
			outRowList = recommendedItemList[recommendedItemList['user_id']==user]
			resultList[user] = list(outRowList['item_id'])
		print resultList
		return json.dumps(resultList)

	else:
		raise Exception('model does not exist.')
		return

if __name__ == "__main__":
	#TODO how to get requested user ?
	modelname = sys.argv[1]
	filename, file_extension = os.path.splitext(modelname)
	fileList = filename.split('_')

	jsonfile = sys.argv[2]
	zipname = modelname + '.zip'

	download("models", zipname)
	
	zip_ref = zipfile.ZipFile(zipname, 'r')
	zip_ref.extractall(modelname)
	zip_ref.close()

	# predict
	# reqUserList = {"userList": ["A3SGXH7AUHU8GW"]}
	with open(jsonfile) as data_file:
		userDict = json.load(data_file)
	#queryList = [str(v) for v in userDict['userList']]
	resultList = predict(modelname, userDict['userList'])

