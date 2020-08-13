import os
import re

### SETUP ###
file_before = 'Localizable_before.strings'
file_after = 'Localizable_after.strings'
cases = ['%d', '%@','\\n', '\\n ']

print('\n')
print('=== START DIFF ERROR PROCESS ===')
print('MATCH CASES: ')
print(cases)
print('\n')

f_before = open(file_before, "r", encoding='UTF-8')
f_after = open(file_after, "r", encoding='UTF-8')

lines_before = f_before.readlines()
lines_after = f_after.readlines()

### Read Data ###
line_before_keys = []
line_before_contents = []
line_after_keys = []
line_after_contents = []

def valuesFromResults(results):
	count = 0
	column0 = '';
	column1 = '';
	for r in results:
		if count == 0:
			column0 = r.replace(' ','')
		if count == 1:
			r = r.replace(' "','')
			r = r.replace('"','')
			column1 = r
		count = count+1

	return (column0, column1)

for line in lines_before:
	### Read Conditions, if not, skip ###
	
	# if line.find('//') != -1:
	
	### Deal with each line ###
	#1: remove ; at last
	line = line[:-2]

	#2: split
	results = re.split(r'=', line) #切等號

	#3: values from results
	values = valuesFromResults(results)

	### save into arr ###
	if values[0] != '' and values[1] != '':
		line_before_keys.append(values[0])
		line_before_contents.append(values[1])

for line in lines_after:
	
	#1: remove ; at last
	line = line[:-2]

	#2: split
	results = re.split(r'=', line) #切等號

	#3: values from results
	values = valuesFromResults(results)
	
	### save into arr ###
	if values[0] != '' and values[1] != '':
		line_after_keys.append(values[0])
		line_after_contents.append(values[1])

### match same keys ###
match_indexs_before = []
match_indexs_after = []

for index_before, key_before in enumerate(line_before_keys):
	if key_before in line_after_keys:
		match_indexs_before.append(index_before)
		match_indexs_after.append(line_after_keys.index(key_before))

### check cases ###

for i, before_index in enumerate(match_indexs_before):
	beforeContent = line_before_contents[before_index]
	afterContent = line_after_contents[match_indexs_after[i]]
	for case in cases:
		if beforeContent.count(case) != afterContent.count(case):
			print('ERROR: %s' % line_before_keys[before_index])
			print('CASE: "%s"'% case)
			print('#1: %s\n#2: %s' % (beforeContent, afterContent))
			print('\n')

print('=== COMPLETE PROCESS ===')
print('\n')





