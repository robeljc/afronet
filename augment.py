import random;
import os;
from os.path import join, getsize

transformations = {'0': ["fliph"], '1': ["noise_0.03","noise_0.02", "noise_0.01"],
						'2': ["rot_-30","rot_-15", "rot_15", "rot_30"], 
						'3': ["blur_0.5", "blur_1.0", "blur_1.5"]}

def transformDirectory(path):
	folders = [fd for fd in os.listdir(path) if os.path.isdir(path+fd)]
	#print folders
	if len(folders) == 0:

		modNum = random.randint(1, len(transformations)) #random number of modifications to image
		copyTrans = transformations.copy()
		script = "python image_augmentor-master/main.py " + path + " "#script to execute

		#print path

		for i in xrange(modNum):
			key, valueList = random.choice(list(copyTrans.items()))
			value = random.choice(valueList)

			script += value
			#print ("copy: ", copyTrans)
			copyTrans.pop(key)

			if ((i+1) != modNum):
				script += ","

		#print script
		os.system(script)

	else:
		for folder in folders:
			transformDirectory(path + folder + '/')

	return;

transformDirectory('./data/')
#print [fn for fn in os.listdir('data/') if os.path.isdir('./data/'+fn)]