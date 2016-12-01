
with open('matrices/pam120.txt') as f:
	lines = f.readlines()
	matrix = {}
	
	aa_list = lines[0].split()
	for i in aa_list:
			matrix[i] = {} 
	for line in lines[1:]:
		data = line.split()
		name = data[0]
		values = data[1:]
		matrix[name] = dict(zip(aa_list, values))
			
def read_pair(a,b):
	return (matrix[a])[b]
