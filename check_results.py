# encode = 'utf-8'
import math
import os

def GetAllValidText():
	files = os.listdir('.')
	validfiles=[]
	for i in files:
		file = i
		index = file.rfind('.')
		if index != -1:
			sufix = file[index:]
			if sufix == '.txt':
				validfiles.append(file)
	return validfiles

def CheckResults(filename):
	fp = open(filename, 'r')
	lines = fp.readlines()
	if len(lines) != 10000:
		print('{} is not 10000 lines'.format(filename))
	start_index = 3
	if len(filename) == 8:
		start_index = 4
	last_index = -1
	nindex = 0
	for i in lines:
		if len(i) < 4:
			continue
		index= i[start_index:(start_index + 4)]
		nindex = int(index)
		if nindex != (last_index + 1):
			print('{} miss or repeat {}'.format(filename,last_index+1))
		last_index = nindex
	if nindex != 9999:
		print('{} not 9999'.format(filename))

allfiles = GetAllValidText()
print(allfiles)
print('have {} valid files'.format(len(allfiles)))
for j in allfiles:
	CheckResults(j)