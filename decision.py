
import math
import copy
import argparse


class Node(object):
	def __init__(self, table, level):
		self.child_nodes = []
		self.table = table
		self.num_yes = None			#positive classification
		self.num_no = None			#negative classification
		self.children = []			# what categories are being expanded
		self.parent = None			# input variable that was expanded one step ahead
		self.expanded_input_catrgory = ""		#what input varaible is expanded in this step
		self.current_category = ""				# what is the current category ex. male if parent was "sex"
		self.answer = None
		self.level = level

	def get_parent(self):
		return self.parent
	def get_expanded_input_category(self):
		return self.expanded_input_catrgory
	def get_current_category(self):
		return self.current_category
	def set_current_category(self, n):
		self.current_category = n
	def set_num_yes(self, n):
		self.num_yes = n
	def set_num_no(self, n):
		self.num_no = n
	def set_parent(self, n):
		self.parent = n 
	def set_expanded_input_category(self, n):
		self.expanded_input_catrgory = n 
	def set_children(self, listt):
		self.children = listt
	def get_table(self):
		return self.table
	def get_num_yes(self):
		return self.num_yes
	def get_num_no(self):
		return self.num_no
	def get_children(self):
		return self.children
	def get_level(self):
		return self.level
	def set_level(self, n):
		self.level = n
	def get_child_nodes(self):
		return self.child_nodes
	def set_child_nodes(self, n):
		self.child_nodes = n
	def get_answer(self):
		return self.answer
	def set_answer(self, n):
		self.answer = n


	# def __str__(self, level =0):
	# 	if self.answer == None:
	# 		txt = "->"*level  +  self.current_category  + "\n" + "   "*(level) + self.expanded_input_catrgory	#+ self.expanded_input_catrgory +": "
	# 		for i in self.child_nodes:
	# 			txt += i.__str__(level+1)
	# 	else:
	# 		txt = "->"*level  +  self.current_category  + ": " + self.answer + "\n" + "   "*(level) + self.expanded_input_catrgory	#+ self.expanded_input_catrgory +": "
	# 		for i in self.child_nodes:
	# 			txt += i.__str__(level+1)
	# 	return txt



def count_yes_no(table):
	count_yes=0
	count_no=0
	for i in range(len(table)):

		if table[i][-1] == "yes":
			count_yes +=1
		if table[i][-1] == "no":
			count_no +=1

	return count_yes, count_no


def make_root(table, level=0):

	root = Node(table, level)
	x,y = count_yes_no(table)
	root.set_num_yes(x)
	root.set_num_no(y)
	# root.set_level(0)
	if x == 0 or y == 0:
		root.set_children([])

	elif len(table[0]) == 1:
		root.set_children([])

	else:
		max_gain = 0
		# index_to_expand = 0
		for i in range(0, len(table[0])-1):
			gain = calculate_gain(table, table[0][i])
			if gain >= max_gain:
				index_to_expand = i
				max_gain = gain
		child = []
		for i in range(1,len(table)):
			if table[i][index_to_expand] not in child:
				child.append(table[i][index_to_expand])
		root.set_children(child)

		root.set_expanded_input_category(table[0][index_to_expand])

	if root.get_children() ==[]:
		x=[]

		for i in range(1,len(table)):
			x.append(table[i][-1])
		total_yes = x.count('yes')
		total_no = x.count('no')
		if total_no < total_yes:
			res = 'yes'
		else:
			res = 'no'
		# print(res)
		root.set_answer(res)
	
	return root


def transition(node, child_name):
	
	table1 = copy.deepcopy(node.get_table())
	
	new_table = []
	new_table.append(copy.deepcopy(table1[0]))
	
	
	input_index = new_table[0].index(node.get_expanded_input_category())
	
	
	for i in range(len(table1)):
		if table1[i][input_index]== child_name:
			
			new_table.append(table1[i])
	
	for i in range(len(new_table)):
		new_table[i].pop(input_index)
	child_node = make_root(new_table, node.get_level()+1)
	child_node.set_parent(node)
	child_node.set_current_category(child_name)
	child_node.set_level(node.get_level()+1)
	
	# print(child_node.get_expanded_input_category())
	# print(child_node.get_children())
	return child_node


def calculate_gain(table, column):
	count_yes = 0
	count_no = 0
	
	label_index = table[0].index(column)
	count_yes, count_no = count_yes_no(table)

	category = []
	for i in range(1,len(table)):
		if table[i][label_index] not in category:
			category.append(table[i][label_index])
	num_category= len(category)
	
	remainder = 0

	for i in category:
		pk=0
		nk=0
		for j in range(1,len(table)):
			
			if table[j][label_index]== i and table[j][-1]=="yes":
				
				pk +=1
			if table[j][label_index]== i and table[j][-1]=="no":
				
				nk +=1

		sub_category_entropy = ((pk+nk)/(count_yes+count_no))*entropy(pk/(pk+nk))
		
		remainder = remainder + sub_category_entropy

	gain_column = entropy(count_yes/(count_yes+count_no)) - remainder

	# new_table = [[] for _ in range(len(table))]

	# for i in range(len(table)):
	# 	for j in range(len(table[0])):
	# 		if j != label_index:
	# 			new_table[i].append(table[i][j])
	return gain_column


def entropy(p):
	if p == 0 or p==1:
		return 0
	else:
		return (-((p* math.log(p,2))+((1-p)*math.log((1-p),2))))

def make_tree(root):
	frontier = []
	frontier.append(root)
	while len(frontier) != 0:
		# print(len(frontier))
		node2expand = frontier.pop(0)
		baby = node2expand.get_children()
		# print("--------------LEVEL----------")
		# print(node2expand.get_children())
		# print(node2expand.get_table())
		if len(baby) != 0 :
			child_node = []
			for i in baby:			
				baby_node = transition(node2expand, i)
				child_node.append(baby_node)
				# print(baby_node.get_current_category(), baby_node.get_expanded_input_category())
				frontier.append(baby_node)
			node2expand.set_child_nodes(child_node)

# def print_tree(root):
# 	# print(root.get_expanded_input_category())
# 	print(str(root))

def prediction(tree, table):
	done = False
	node = tree
	while done == False:
		# print(node.get_expanded_input_category())
		# print(table)
		# print(node.get_expanded_input_category())
		if node.get_expanded_input_category() != "":
			ind = table[0].index(node.get_expanded_input_category())
			# print(ind)


		if node.get_children() ==[]:
		 	answer = node.get_answer()
		 	# print(answer)
		 	done = True
		 	break

		# print(table[1][ind])
		if table[1][ind] in node.get_children():
		 	ind1 = node.get_children().index(table[1][ind])
		 	node = node.get_child_nodes()[ind1]
		 	# print(node.get_current_category())

		else:
		 	answer = "no"
		 	done =True
	return answer

def test_set_accuracy(table):
	accuracy = 0
	for i in range(1, len(table)):
		test = [[]]
		train = copy.deepcopy(table)
		test[0] = copy.deepcopy(train[0])
		test.append(train.pop(i))
		# print(train, "\n",  test)
		root = make_root(train)
		make_tree(root)

		answer = prediction(root, test)

		# print(test, "\n", answer)
		if answer == test[1][-1]:
			accuracy +=1

	accuracy = accuracy/(len(table)-1)
	return accuracy

def train_set_accuracy(table):
	accuracy = 0
	root = make_root(table)
	make_tree(root)
	
	
	for i in range(1, len(table)):
		test = [[]]
		test[0] = copy.deepcopy(table[0])
		test.append(table[i])
		answer = prediction(root, test)

		if answer == test[1][-1]:
			accuracy +=1

	accuracy = accuracy/(len(table)-1)
	return accuracy


def print_tree(root):
	expanded =[]
	expanded.append(root)
	# print(node.get_expanded_input_category())
	while len(expanded) != 0:

		node2expand = expanded.pop(len(expanded)-1)

		if node2expand.get_current_category() != "":
			print("\t"*node2expand.get_level() + node2expand.get_current_category())

		print("\t"*node2expand.get_level() + node2expand.get_expanded_input_category() + ":")

		for i in node2expand.get_child_nodes():
			
			expanded.append(i)
		if len(node2expand.get_child_nodes()) == 0:
			print("\t"*node2expand.get_level() + "-->" +node2expand.get_answer())









def read_file(filename):
	file=open(filename,"r")
	table=[]
	for i in file:
		line=i.split("\t")
		line[-1]=line[-1].rstrip()
		table.append(line)
	return table

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("file")
	args=parser.parse_args()
	file_name= args.file


	table = read_file(file_name)
	root = make_root(table)
	make_tree(root)
	# print_tree(root)
	# print(file_name)
	print_tree(root)
	print("train set validation = ", train_set_accuracy(table))
	print("test set validation = " , test_set_accuracy(table))
	# full_test(table)
	# j = prediction(root,[['size', 'color', 'earshape', 'tail', 'iscat'], ['small', 'orange', 'pointed', 'yes', 'yes']])
	# print(j)
	

	


