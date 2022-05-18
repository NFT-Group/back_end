import json

# Note: this is still using csvs, needs modification to work with json

historical_data = []
with open("/home/henry/dev/group_project/data/historical_data/past_0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv", encoding = "ascii") as f:
	for line in f:
		historical_data.append(line.split('|'))
# historical_data.sort(key=lambda x: int(x[6]))

metadata = []
with open("/home/henry/dev/group_project/data/metadata/all_0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B.csv", encoding = "utf-8") as f:
	for line in f:
		metadata.append(tuple(line.split('|')))

meta_dict = dict()
for i, j in metadata:
	meta_dict.setdefault(int(i), j)

for i, j in meta_dict.items():
	meta_dict[i] = json.loads(meta_dict[i])

def union(lst1, lst2):
    lst3 = lst1 + lst2
    return lst3 	

def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3

def attr_search(attr_ls): #param: list of strs

	attr_dict = {}
	[attr_dict.setdefault(at, []) for at in attr_ls]

	for enum, key in enumerate(meta_dict):
		for attr in meta_dict[key]["attributes"]:
			for at in attr_ls:
				if at in attr["value"]:
					attr_dict[at].append(meta_dict[key]["name"])
	
	unique = []
	for key in attr_dict:
		unique = union(unique, attr_dict[key])
	
	for key in attr_dict:
		unique = intersection(unique, attr_dict[key])
	unique = set(unique)
	print(unique)

def find_whales(top):

	# Prune the null-addr purchasers
	clean_hist = [i for i in historical_data if i[-2] != '0']

	# Make dict {purchasers:[total_purchases,total_value]}
	
	print(clean_hist)

find_whales(10)
