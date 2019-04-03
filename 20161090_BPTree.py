import sys,os
import bisect


# Stores results
output_buffer = []

class BPlusTree:

	def __init__(self, factor):
		self.factor = factor
		self.root = Node()
	
	def insert_routine(self, key):

		# Start inserting key
		ans, newNode =  self.tree_insert(key, self.root)

		if not ans:
			tempCount = 0
		else:
			newRoot = Node()
			newRoot.is_leaf = False
			newRoot.keys = [ans]
			newRoot.children = [self.root, newNode]
			self.root = newRoot

	def bisectArray(self, node, key):
		index = bisect.bisect(node.keys, key)
		node.keys[index:index] = [key]
		return index

	def tree_insert(self, key, node):

		if node.is_leaf:
			index = self.bisectArray(node,key)
			node.children[index:index] = [key]

			nodeLen = len(node.keys)
			
			if nodeLen <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode

		if key < node.keys[0]:
			ans, newNode = self.tree_insert(key, node.children[0])
		
		loopRange = len(node.keys) - 1

		for i in range(loopRange):
			if key >= node.keys[i] and key < node.keys[i + 1]:
				ans, newNode = self.tree_insert(key, node.children[i+1])
		
		nodeKeyLength = len(node.keys)
		nodeChildLength = len(node.children)
		if key >= node.keys[nodeKeyLength-1]:
			ans, newNode = self.tree_insert(key, node.children[nodeChildLength-1])

		if ans:
			index = self.bisectArray(node,ans)
			indexUpdate = index+1
			node.children[indexUpdate:indexUpdate] = [newNode]
			if len(node.keys) > self.factor-1:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		
		return None, None

	def tree_search_for_query(self, key, node):

		if not node.is_leaf:
			if key <= node.keys[0]:
				return self.tree_search_for_query(key, node.children[0])
			
			loopRange = len(node.keys)-1
			for i in range(loopRange):
				if key>node.keys[i] and key<=node.keys[i+1]:
					return self.tree_search_for_query(key, node.children[i+1])
			
			nodeKeyLength = len(node.keys)
			nodeChildLength = len(node.children)			
			
			if key > node.keys[nodeKeyLength-1]:
				return self.tree_search_for_query(key, node.children[nodeChildLength-1])
		else:
			return node


	def get_keys_in_range(self, keyMin, keyMax, node):

		count = 0
		nodeLength = len(node.keys)

		for i in range(nodeLength):
			key = node.keys[i]
			if keyMin <= key and key <= keyMax:
				count = count+1

		nodeLength = len(node.keys)
		
		if not nodeLength:
			return nodeLength, None

		if node.keys[-1] > keyMax:
			next_node = None

		else:
			if node.next:
				next_node = node.next
			else:
				next_node = None
		return count, next_node
	
	def count_query(self, key):

		count = 0
		start_leaf = self.tree_search_for_query(key, self.root)

		key_count, next_node = self.get_keys_in_range(key, key, start_leaf)
		count = count + key_count

		while next_node:
			key_count, next_node = self.get_keys_in_range(key, key, next_node)
			count += key_count

		return count

	def range_query(self, keyMin, keyMax):

		count = 0
		start_leaf = self.tree_search_for_query(keyMin, self.root)

		key_count, next_node = self.get_keys_in_range(keyMin, keyMax, start_leaf)
		count += key_count

		while next_node is not None:
			key_count, next_node = self.get_keys_in_range(keyMin, keyMax, next_node)
			count += key_count

		return count

class Node:

	def __init__(self):
		
		# Initialize a node with no children or keys and taking it a leaf node
		self.children = []
		self.keys = []
		self.is_leaf = True
		self.next = None

	def splitNode(self):
		newNode = Node()

		keyLength = len(self.keys)
		
		if not self.is_leaf:
			newNode.is_leaf = False

			midKey = self.keys[keyLength/2]

			newNode.keys = self.keys[keyLength/2+1:]
			newNode.children = self.children[keyLength/2+1:]

			# Update keys and children of node
			self.keys = self.keys[:keyLength/2]
			self.children = self.children[:keyLength/2 + 1]
			return midKey, newNode

		else:
			newNode.is_leaf = True

			midKey = self.keys[keyLength/2]

			newNode.keys = self.keys[keyLength/2:]
			newNode.children = self.children[keyLength/2:]

			# Update keys and children of node
			self.keys = self.keys[:keyLength/2]
			self.children = self.children[:keyLength/2]

			newNode.next = self.next
			self.next = newNode
			return midKey, newNode
		
		return None

def perform(cmnd):
	global output_buffer

	if cmnd[0].upper() == "INSERT":
		tree.insert_routine(int(cmnd[1]))

	elif cmnd[0].upper() == "FIND":
		res = tree.count_query(int(cmnd[1]))
		if res == 0:
			#print "NO"
			output_buffer.append("NO")
		else:
			#print "YES"
			output_buffer.append("YES")

	elif cmnd[0].upper() == "COUNT":
		res = tree.count_query(int(cmnd[1]))
		#print res
		output_buffer.append(str(res))

	elif cmnd[0].upper() == "RANGE":
		res = tree.range_query(int(cmnd[1]), int(cmnd[2]))
		#print res
		output_buffer.append(str(res))

	if len(output_buffer) >= ((B * 1.0) / 10.0):
		for res in output_buffer:
			print(res)
		output_buffer = []

def runQuery(input):
	for command in input:
		perform(command)

# Start Program
# Input from command
filename = sys.argv[1]
M = int(sys.argv[2])
B = int(sys.argv[3])
# Check if file exists
if os.path.isfile(filename):
	
	input_buffer = []

	# Count number of pointers
	pointerCount = ((B - 8) / 12) + 1
	if pointerCount <= 2:
		pointerCount = 2

	# Initialize root node
	tree = BPlusTree(pointerCount)
	
	# Start reading file
	with open(filename) as fh:
		for line in fh:
			cmnd = line.strip().split()
			input_buffer.append(cmnd)

			# If buffer array exceeds the total memory allocated
			if len(input_buffer) >= (((M-1) * B * 1.0) / 10.0) :
				runQuery (input_buffer)
				# Empty buffer
				input_buffer = []
	fh.close()
	
	# Running remaining buffer
	runQuery (input_buffer)

	# Print result
	for result in output_buffer:
		print(result)

# If file does not exist
else:
	print("Invalid File")
	exit(-1)

