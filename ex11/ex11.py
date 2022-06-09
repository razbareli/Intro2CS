##########################################################
# FILE:ex11.py
# WRITER:Raz_Bareli unixraz 203488747
# EXERCISE:intro2cs1 ex11 2021
# DESCRIPTION: Graphs
##########################################################

import itertools

class Node:
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child

class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms
	
			
def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records


class Diagnoser:
	def __init__(self, root: Node):
		self.root = root

	def diagnose(self, symptoms):
		return self.diagnose_helper(symptoms, self.root)

	def diagnose_helper(self, symptoms, root):
		if root.positive_child is None and root.negative_child is None:
			return root.data
		else:
			if root.data not in symptoms:
				return self.diagnose_helper(symptoms, root.negative_child)
			else:
				return self.diagnose_helper(symptoms, root.positive_child)

	def calculate_success_rate(self, records):
		tot_records = len(records)
		if tot_records == 0:
			raise ValueError("There are no records")
		tot_success = 0
		for i in records:
			if i.illness == self.diagnose(i.symptoms):
				tot_success += 1
		return tot_success/tot_records

	def all_illnesses(self):
		illnesses = dict()
		self.all_illnesses_helper(self.root, illnesses)
		lst = [illnesses[i] for i in illnesses]
		final_lst = []
		if not lst:
			return lst
		for i in range(max(lst), 0, -1):
			for j in illnesses:
				if illnesses[j] == i:
					final_lst.append(j)
		return final_lst

	def all_illnesses_helper(self, root, illnesses):
		if root is None or root.data is None:
			return []
		if root.positive_child is None and root.negative_child is None and root.data is not None:
			if root.data not in illnesses:
				illnesses[root.data] = 1
			else:
				illnesses[root.data] += 1
		else:
			self.all_illnesses_helper(root.positive_child, illnesses)
			self.all_illnesses_helper(root.negative_child, illnesses)

	def paths_to_illness(self, illness):
		return self.paths_to_illness_helper(self.root, [], [], illness)

	def paths_to_illness_helper(self, root, temp, final, illness):
		if root.positive_child:
			temp.append(True)
			self.paths_to_illness_helper(root.positive_child, temp, final, illness)
		if root.negative_child:
			temp.append(False)
			self.paths_to_illness_helper(root.negative_child, temp, final, illness)
		if not root.positive_child and not root.negative_child and root.data == illness:
			final.append(temp[:])
		if temp:
			temp.pop()
		else:
			return final

	def minimize(self, remove_empty=False):
		if not remove_empty:
			self.root = self.minimize_helper_false(self.root)
		else:
			self.root = self.minimize_helper_true(self.root)
			self.root = self.minimize_helper_false(self.root)


	def minimize_helper_false(self, root: Node, is_positive_child=True):
		if root.positive_child:
			root.positive_child = self.minimize_helper_false(root.positive_child, True)
			root.negative_child = self.minimize_helper_false(root.negative_child, False)
			temp = self.minimize_helper_1(root, list())
			temp_len = len(temp)
			if temp_len % 2 == 0:
				left_data = [node.data for node in temp[:temp_len//2]]
				right_data = [node.data for node in temp[temp_len//2:]]
				if left_data == right_data:
					if is_positive_child:
						root = root.positive_child
					else:
						root = root.negative_child
		return root

	def minimize_helper_true(self, root: Node, is_positive_child=True):
		if root.positive_child:
			root.positive_child = self.minimize_helper_true(root.positive_child, True)
			root.negative_child = self.minimize_helper_true(root.negative_child, False)
			temp = self.minimize_helper_1(root, list())
			temp_data = [node.data for node in temp]
			if None in temp_data:
				if temp_data.index(None) == 0:
					root = root.negative_child
				else:
					root = root.positive_child
		return root


	def minimize_helper_1(self, root, bucket):
		if not root.positive_child:
			bucket.append(root)
		else:
			self.minimize_helper_1(root.positive_child, bucket)
			self.minimize_helper_1(root.negative_child, bucket)
		return bucket

def build_tree(records, symptoms):
	for i in records:
		if type(i) is not Record:
			raise TypeError("object in records is not from type Record")
	for j in symptoms:
		if type(j) is not str:
			raise TypeError("object in symptoms is not from type str")
	return Diagnoser(build_tree_helper(records, symptoms, None, 0, len(symptoms), ""))


def build_tree_helper(records, symptoms, root, curr, length, path):
	if curr < length:
		root = Node(symptoms[curr])
		root.positive_child = build_tree_helper(records, symptoms, root.positive_child, curr + 1, length, path+" T")
		root.negative_child = build_tree_helper(records, symptoms, root.negative_child, curr + 1, length, path+" F")
	else:
		way = path.split(" ")
		way = way[1:]
		poss = []
		for j in records:
			temp = True
			for i in range(len(symptoms)):
				if way[i] == "T":
					if symptoms[i] not in j.symptoms:
						temp = False
				if way[i] == "F":
					if symptoms[i] in j.symptoms:
						temp = False
			if temp:
				poss.append(j.illness)
		if not poss:
			root = Node(None)
		else:
			final = most_frequent(poss)
			root = Node(final)
	return root

def most_frequent(lst):
	"""finds the most frequent object in a given list"""
	dic = dict()
	for i in lst:
		if i not in dic:
			dic[i] = 1
		else:
			dic[i] += 1
	freq = [dic[i] for i in dic]
	m = max(freq)
	for i in dic:
		if dic[i] == m:
			return i

def optimal_tree(records, symptoms, depth):
	if depth < 0 or depth > len(symptoms):
		raise ValueError("the value of depth is not valid")
	tree = []
	success = []
	all_subsets = list(itertools.combinations(symptoms,depth))
	for i in all_subsets:
		temp_tree = build_tree(records, i)
		temp_success = temp_tree.calculate_success_rate(records)
		tree.append(temp_tree.root)
		success.append(temp_success)
	m = success.index(max(success))
	root = tree[m]
	return Diagnoser(root)

