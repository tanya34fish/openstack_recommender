import sys
import os
import graphlab as gl
from swift_wrapper import upload_from_file, download

def splitData(dataname):
	data = {}
	train = {}
	test = {}
	trainfile = 'train.tmp'
	testfile = 'valid.tmp'
	firstLine = ''
	with open(dataname, 'r') as f:
		firstLine = f.readline()
		for line in f:
			k = line.strip().split(',')
			if k[0] not in data:
				data[k[0]] = []
			data[k[0]].append((k[1],k[2]))

	for user, itemList in data.iteritems():
		trainLen = 4 * len(itemList) / 5
		if trainLen < 5:
			train[user] = itemList
		else:
			train[user] = itemList[:trainLen]
			test[user] = itemList[trainLen:]
	
	with open(trainfile, 'w') as f:
		f.write(firstLine)
		for user, itemList in train.iteritems():
			for item in itemList:
				f.write('%s,%s,%s\n' %(user,item[0],item[1]))
	
	with open(testfile, 'w') as f:
		f.write(firstLine)
		for user, itemList in test.iteritems():
			for item in itemList:
				f.write('%s,%s,%s\n' %(user,item[0],item[1]))
	return

def convertData(data):
	userIdList = []
	itemIdList = []
	ratingList = []
	for user, itemList in data.iteritems():
		for (item,rating) in itemList:
			userIdList.append(user)
			itemIdList.append(item)
			ratingList.append(rating)

	newdata = gl.SFrame({'user_id': userIdList, 'item_id': itemIdList, 'rating': ratingList})
	print newdata
	return newdata

def createModel(data, filename, hasRating, modeltype='default'):
	import shutil

	if modeltype == 'default':
		if hasRating:
			model = gl.recommender.create(data, user_id='user_id', item_id='item_id', target='rating')
		else:
			model = gl.recommender.create(data, user_id='user_id', item_id='item_id')

	elif modeltype == 'item_similarity':
		if hasRating:
			model = gl.item_similarity_recommender.create(data, target='rating', similarity_type='cosine')
		else:
			model = gl.item_similarity_recommender.create(data, similarity_type='cosine')
	
	elif modeltype == 'popularity':
		if hasRating:
			model = gl.popularity_recommender.create(data, target='rating')
		else:
			model = gl.popularity_recommender.create(data)

	elif modeltype == 'mf':
		if hasRating:
			model = gl.ranking_factorization_recommender.create(data, target='rating')
		else:
			model = gl.ranking_factorization_recommender.create(data)
	
	modelname = filename + '_' + modeltype + '.model'
	model.save(modelname)
	shutil.make_archive(modelname, 'zip', modelname)
	upload_from_file("models", modelname + '.zip')
	return
	
if __name__ == "__main__":
	dataname = sys.argv[1]
	modeltype = 'default'
	if len(sys.argv) == 3:
		modeltype = sys.argv[2]

	filename, file_extension = os.path.splitext(dataname)
	
	download("data", dataname)
	with open(dataname, 'r') as f:
		columnName = f.readline()
	columnNameList = columnName.strip().split(',')

	
	hasRating = False
	if "rating" in columnNameList:
		trainSFrame = gl.SFrame.read_csv(dataname, column_type_hints={"rating":int})
		hasRating = True
	else:
		trainSFrame = gl.SFrame.read_csv(dataname)

	createModel(trainSFrame, filename, hasRating, modeltype=modeltype)
	
	# predict
	#reqUserList = ["Jacob Smith", "Zion Smith"]
	#resultList = predict(model, reqUserList)
	#print resultList
