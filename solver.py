import csv
from sys import stdout
from rule_structure import Statement, rules

FILENAME = "result.log"
LEFT = 1
RIGHT = 2
OVER = 3
UNDER = 4 
EVERYWHERE = 5

'''
Set this variable to 'True' to force the nodes to stay on the same line
set it to false to avoid that.

Example: 
STRICT = True
A,x=0,y=0 Left B,x=1,y=0 ? --> True
A,x=0,y=0 Left B,x=1,y=1 ? --> False

STRICT = False
A,x=0,y=0 Left B,x=1,y=0 ? --> True
A,x=0,y=0 Left B,x=1,y=1 ? --> True

'''
#TODO: still not implemented
STRICT = True 
IN_LINE = True
'''
def verify_rule(node1, rule, node2):
	if RIGHTRULE == STRICT:
		
	else:
'''
def opposite(rule):
	return {
		LEFT: RIGHT,
		RIGHT: LEFT,
		OVER: UNDER,
		UNDER: OVER,
	}[rule]

class Node(object):
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name
		#self.myhash = None

	def __str__(self):
		return str((self.x,self.y, self.name))
		
	'''def __repr__(self):
		return str((self.x,self.y))
	
	def __hash__(self):
		if self.myhash != None:
			return self.myhash
		self.myhash = hash(''.join(self.l)+','+''.join(self.s)+','+''.join(self.r))	
		return self.myhash
		
	def human_readable(self):
		return  "--------"+str(self.depth +1)+"---------\n" + ''.join(self.l) + " ==>\t<== " + ''.join(reversed(self.r)) +"\n\t<== " +''.join(reversed(self.s)) 

	def linear_repr(self):
		return "["+''.join(self.l)+','+''.join(reversed(self.s))+','+''.join(reversed(self.r))+"]"'''


def getNodeFromLabel(nodes, label):
	for nodo in nodes:
		if nodo.name == label:
			return nodo
	print "Label not found"
	return None	
	
def filtro(plan, label1, rule, label2):
	n1 = getNodeFromLabel(plan, label1)
	n2 = getNodeFromLabel(plan, label2)
	print "filter n1" + str(n1)
	print "filter n2" + str(n2)

	for i in range(len(plan)):
		if plan[i].name == label1:
			n1 = plan[i]
		elif plan[i].name == label2:
			n2 = plan[i]
	if rule == LEFT:
		if n1.y == n2.y and n1.x < n2.x:
			return True
		return False
	elif rule == RIGHT:
		if n1.y == n2.y and n1.x > n2.x:
			return True
		return False
	elif rule == OVER:
		if n1.x == n2.x and n1.y > n2.y:
			return True
		return False	
	elif rule == UNDER:
		if n1.x == n2.x and n1.y > n2.y:
			return True
		return False

def equalizer(plan, origin):
	skew_x = 0
	skew_y = 0
	for node in plan:
		if node.name == origin.name:
			skew_x = node.x -origin.x
			skew_y = node.y -origin.y
	for node in plan:
		node.x = node.x - skew_x
		node.y = node.y - skew_y
	return plan
	
def equalize_plans(plans):
	equalizeds = []
	if plans != [] and plans[0] != None:
		#label = plans[0][0]
		for plan in plans:
			equalizeds.append(equalizer(plan, plans[0][0]))
		return equalizeds
	else: 
		print "Error empty plans!"
		return None

def plans_eq(plan1, plan2):
	if len(plan1) != len(plan2):
		return False
	eq = True
	for nodo1 in plan1:
		nodo2 = getNodeFromLabel(plan2, nodo1.name)
		if nodo2 == None:
			return False
		else:
			eq = eq and nodo2.x == nodo1.x and nodo2.y == nodo1.y
			if not eq:
				return False
			
	return eq
	
def make_set(plans):
	newplans = []
	for plan in plans:
		present = False
		for new_plan in newplans:
			if plans_eq(plan, new_plan):
				present = True
		if not present:
			newplans.append(plan)
	return newplans

def genChildren(nodes, label1, rule, label2):
	node1 = getNodeFromLabel(nodes, label1)
	node2 = getNodeFromLabel(nodes, label2)
	print "label1 "+str(label1)
	print "label2 "+str(label2)
	print "lnodes "+str(len(nodes))
	print "node1 "+str(node1)
	print "node2 "+str(node2)
	print "-.-.-."
	for elem in nodes:
		print "nodo: "+str(elem)
	print "-.-.-."
	plans = []
	label = None
	node = None
	
	everywhere = False
	
	#board vuota
	if nodes == []:
		print "Inizializing board"
		plans.append(nodes)
		label = label1
		node = Node(0,0,label2)
		nodes.append(node)
	#un nodo trovato
	elif node1 != None and node2 == None:
		print "One node found A"
		node = node1
		rule = opposite(rule)
		label = label2
		plans.append(nodes)
	#l'altro nodo trovato
	elif node1 == None and  node2 != None:
		print "One node found B"
		node = node2
		label = label1
		plans.append(nodes)
	#entrambi i nodi trovati
	elif node1 != None and node2 != None:
		print "Two nodes found"
		plans = []
		if filtro(nodes, label1, rule, label2):
			yield nodes
	#nessun nodo trovato e board non vuota
	else:
		print "n1"+str(node1)
		print "n2"+str(node2)
		print "Nodes not found, board not empty"
		
		for plan in addOneNode(nodes, label2, EVERYWHERE, None):
			plans.append(plan)
		plans = equalize_plans(plans)
		print "pl0: "+ str(len(plans))
		plans = make_set(plans)
		print "pl1: "+ str(len(plans))
		redundant_plans = []
		for plan in plans:
			for nodus in addOneNode(plan, label1, rule,  getNodeFromLabel(plan, label2)):
				redundant_plans.append( nodus)
		print "rp0: "+ str(len(redundant_plans))
		plans = []
		
		for plan in addOneNode(nodes, label1, EVERYWHERE, None):
			plans.append(plan)
		plans = equalize_plans(plans)
		plans = make_set(plans)
		for plan in plans:
			for nodus in addOneNode(plan, label2, opposite(rule),  getNodeFromLabel(plan, label1)):
				redundant_plans.append( nodus)
		print "rp1: "+ str(len(redundant_plans))
		redundant_plans = equalize_plans(redundant_plans)
		redundant_plans = make_set(redundant_plans)
		print "rp2: "+ str(len(redundant_plans))
		
		#TODO: orribile!
		for plan in redundant_plans:
			yield plan
		
		plans = []
			
	for plan in plans:
		#se abbiamo generato piu piani bisogna trovare uno ad uno il nuovo nodo
		if everywhere:
			node = getNodeFromLabel(plan, label2)
		for nodus in addOneNode(plan, label, rule, node):
			yield nodus
'''	if everywhere and rule == LEFT:
		edge_element = True
		for i in range(len(nodes)):
			for j in range(len(nodes)):
				if	nodes[i].x == nodes[j].x - 1 and nodes[i].y == nodes[j].y:
					edge_element = False
			if edge_element:
				pass'''
			

def genLeft(nodo, node1, new_label, newnodes):
	newnode = Node(nodo.x -1, nodo.y, new_label)
	for tomove in newnodes:
		if tomove.x <= newnode.x and tomove.y == newnode.y and tomove != node1:
			tomove.x = tomove.x -1
	newnodes.append(newnode)
	return newnodes

def genRight(nodo, node1, new_label, newnodes):
	newnode = Node(nodo.x +1, nodo.y, new_label)
	for tomove in newnodes:
		if tomove.x >= newnode.x and tomove.y == newnode.y and tomove != node1:
			tomove.x = tomove.x + 1
	newnodes.append(newnode)
	return newnodes

def genUnder(nodo, node1, new_label, newnodes):
	newnode = Node(nodo.x, nodo.y-1, new_label)
	for tomove in newnodes:
		if tomove.y <= newnode.y and tomove.x == newnode.x  and tomove != node1:
			tomove.y = tomove.y - 1
	newnodes.append(newnode)
	return newnodes

def genOver(nodo, node1, new_label, newnodes):
	newnode = Node(nodo.x, nodo.y+1, new_label)
	for tomove in newnodes:
		if tomove.y >= newnode.y and tomove.x == newnode.x and tomove != node1:
			tomove.y = tomove.y + 1
	newnodes.append(newnode)
	return newnodes
	
def clonePlan(oldplan):	
	newplan = []
	for old_node in oldplan:
		newplan.append(Node(old_node.x,old_node.y,old_node.name))
	return newplan
			
def addOneNode(nodes, new_label, rule, node1):	
	for nodo in nodes:
		#FIXME! Se fosse programmato meglio non ce ne sarebbe bisogno! I vari gen non dovrebbero 
		# toccacciare le variabili in ingresso
		newnodes = clonePlan(nodes)
		
		#newnodes = nodes[:]
		if rule == EVERYWHERE:
			yield genLeft(nodo, node1, new_label, newnodes)
			newnodes = clonePlan(nodes)
			yield genRight(nodo, node1, new_label, newnodes)
			if not IN_LINE:
				newnodes = clonePlan(nodes)
				yield genUnder(nodo, node1, new_label, newnodes)
				newnodes = clonePlan(nodes)
				yield genOver(nodo, node1, new_label, newnodes)
		
		else:
			if rule == RIGHT and nodo.y == node1.y and nodo.x >= node1.x:
				yield genRight(nodo, node1, new_label, newnodes)
	
			elif rule == UNDER and nodo.x == node1.x and nodo.y <= node1.y:	
				yield genUnder(nodo, node1, new_label, newnodes)
			
			elif rule == OVER and nodo.x == node1.x and nodo.y >= node1.y:	
				yield genOver(nodo, node1, new_label, newnodes)
				
			elif rule == LEFT and nodo.y == node1.y and nodo.x <= node1.x :
				yield genLeft(nodo, node1, new_label, newnodes)
	
relDic = {'left': 'l', 'right': 'r'}

def analyzeStatement(inp):
	vals = inp.split()
	if (len(vals) == 3):
		if vals[1] == 'right':
			return Statement(vals[2], relDic['left'], vals[0])
		return Statement(vals[0], relDic[vals[1]], vals[2])

def generateGraph(name, data):
	goal = analyzeStatement(data[-1])
	if goal.relation == 'r':
		goal = Statement(goal.ropperand, 'l', goal.lopperand)

	for s in data[:-1]:
		st = analyzeStatement(s)
		if st:
			if st.relation == "l":
				yield (st.lopperand,LEFT,st.ropperand)
			else: 
				yield (st.lopperand,RIGHT,st.ropperand)

def main():
	nodes = []
	rules = []
	with open('./experimental_data.csv', 'r') as csvfile:
		#with open('../Data/test.csv', 'r') as csvfile:
		csvFile = csv.reader(csvfile, delimiter=',', quotechar='"')
		next(csvFile)                                                                    # skip headder
		for row in csvFile:
			stdout.write('.')
			stdout.flush()
			print "ROW ", row[2], row[3:7]
			if not rules:
				for rule in generateGraph(row[2], row[3:7]):
					rules.append(rule)
	
	stdout.write('\n')
	stdout.flush()
	'''nodes.append(Node(0,0,'A'))
	print nodes[0]'''
	rules = [['B', LEFT, 'A'],['D', LEFT, 'C']]
	plans = []
	
	rule = rules.pop()
	print "rulla "+str(rule[1])
	for next_plan in genChildren(nodes, rule[0], rule[1], rule[2]):
			plans.append(next_plan)
			print "A plan:" + str(next_plan)
			for node in next_plan:
				print "Node of the plan: " + str(node)
			print "-----"
	
	while rules != [] and plans != [] :
		print "While!!"
		rule = rules.pop()
		print "rulla "+str(rule[1])
		new_plans = []
		for plan in plans:
			print "OLD plan:" + str(plan)
			for node in plan:
				print "Node of the plan: " + str(node)
			print "-----"
				
			for next_plan in genChildren(plan, rule[0], rule[1], rule[2]):
				new_plans.append(next_plan)
				print "A plan:" + str(next_plan)
				for node in next_plan:
					print "Node of the plan: " + str(node)
				print "-----"
		plans = new_plans[:]
'''			
	for plan in plans:
		for next_plan in genChildren(plan, 'C', OVER, 'A'):
			print "A plan:"
			for node in next_plan:
				print(node)
			print "-----"'''

			
main()


	

	


