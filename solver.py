from collections import deque
from random import shuffle
import time

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
STRICT = True

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
	
	
def genChildren(nodes, label1, rule, label2):
	node1 = getNodeFromLabel(nodes, label1)
	node2 = getNodeFromLabel(nodes, label2)
	print "label1 "+str(label1)
	print "label2 "+str(label2)
	print "lnodes "+str(len(nodes))
	print "node1 "+str(node1)
	print "node2 "+str(node2)
	
	plans = []
	label = None
	node = None
	
	#board vuota
	if nodes == []:
		print "Inizializing board"
		plans.append(nodes)
		label = label1
		node = Node(0,0,label2)
		nodes.append(node)
	#un nodo trovato
	elif node1 != None and node2 == None:
		print "One node found"
		node = node1
		label = label2
		plans.append(nodes)
	#l'altro nodo trovato
	elif node1 == None and  node2 != None:
		print "One node found"
		node = node2
		label = label1
		rule = opposite(rule)
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
		for plan in addOneNode(nodes, label1, EVERYWHERE, None):
			plans.append(plan)
		plans = equalize_plans(plans)
		plans = make_set(plans)
		label  = label2
				
	for plan in plans:
		for node in addOneNode(plan, label, rule, node):
			yield node
	
def addOneNode(nodes, new_label, rule, node1):	
	newnodes = None
	for nodo in nodes:
		if rule == LEFT or rule == EVERYWHERE:
			if rule == EVERYWHERE or nodo.y == node1.y and nodo.x <= node1.x :
				newnode = Node(nodo.x -1, nodo.y, new_label)
				newnodes = nodes[:]
				for tomove in newnodes:
					if tomove.x <= newnode.x and tomove != node1:
						tomove.x = tomove.x -1
				newnodes.append(newnode)
				yield newnodes
		
		elif rule == RIGHT or rule == EVERYWHERE:
			if rule == EVERYWHERE or nodo.y == node1.y and nodo.x >= node1.x:
				newnode = Node(nodo.x +1, nodo.y, new_label)
				newnodes = nodes[:]
				for tomove in newnodes:
					if tomove.x >= newnode.x and tomove != node1:
						tomove.x = tomove.x + 1
				newnodes.append(newnode)
				yield newnodes

		elif rule == UNDER or rule == EVERYWHERE:	
			if rule == EVERYWHERE or nodo.x == node1.x and nodo.y <= node1.y:	
				newnode = Node(nodo.x, nodo.y-1, new_label)
				newnodes = nodes[:]
				for tomove in newnodes:
					if tomove.y <= newnode.y and tomove != node1:
						tomove.y = tomove.y - 1
				newnodes.append(newnode)
				yield newnodes
		
		elif rule == OVER or rule == EVERYWHERE:
			if rule == EVERYWHERE or nodo.x == node1.x and nodo.y >= node1.y:	
				newnode = Node(nodo.x, nodo.y+1, new_label)
				newnodes = nodes[:]
				for tomove in newnodes:
					if tomove.y >= newnode.x and tomove != node1:
						tomove.y = tomove.y + 1
				newnodes.append(newnode)
				yield newnodes
	
def main():
	nodes = []
	'''nodes.append(Node(0,0,'A'))
	print nodes[0]'''
	rules = [['B', RIGHT, 'A'],['B', LEFT, 'A']]
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
			for next_plan in genChildren(nodes, rule[0], rule[1], rule[2]):
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

def equalizer(plan, origin):
	skew_x = 0
	skew_y = 0
	for i in range(len(plan)):
		if plan[i].name == origin.name:
			skew_x = plan[i].x -origin.x
			skew_y = plan[i].y -origin.y
	for i in range(len(plan)):
		plan[i].x = plan[i].x - skew_x
		plan[i].y = plan[i].y - skew_y
	return plan
	
def equalize_plans(plans):
	equalizeds = []
	if plans != [] and plans[0] != None:
		label = plan[0][0]
		for plan in plans:
			equalizeds.append(equalizer(plan, plans[0][0]))
		return equalizeds
	else: 
		print "Error empty plans!"
		return None
	
def make_set(plans):
	newplans = []
	for i in range(len(plans)):
		present = False
		for j in range(len(newplans)):
			if plans_eq(plans[i], newplans[j]):
				present = True
		if not present:
			newplans.append(plans[i])
	return newplans
	
def plans_eq(plan1, plan2):
	if len(plan1) != len(plan2):
		return False
	for i in range(len(plan1)):
		eq = False
		for j in range(len(plan2)):
			if plan1[i] == plan2[j]:
				eq = True
		if not eq:
			return False
	return True
	


