from collections import deque
from random import shuffle
import time

FILENAME = "result.log"
LEFT = 1
RIGHT = 2
OVER = 3
UNDER = 4

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
		print "Nodo in getnodes: "+ str(nodo)
		print nodo.name + "--" +label
		if nodo.name == label:
			return nodo
	print "Error in getNodeFromLabel, label not found"
	return None	
	
	
def genChildren(nodes, new_label, rule, old_label):
	old_node = getNodeFromLabel(nodes, old_label)
	#TODO: 
	# inserim primo nodo,
	# 2 nodi presenti
	# nessun nodo presente, ma board non vuota
	
	newnodes = None
	for nodo in nodes:
		print nodo
		if rule == LEFT:
			if nodo.y == old_node.y and nodo.x <= old_node.x:
				newnode = Node(nodo.x -1, nodo.y, new_label)
				newnodes = nodes[:]
				for newnodo in newnodes:
					if newnodo.x <= newnode.x:
						newnodo.x = newnodo.x -1
				newnodes.append(newnode)
				yield newnodes
		
		elif rule == RIGHT:
			if nodo.y == old_node.y and nodo.x >= old_node.x:
				newnode = Node(nodo.x +1, nodo.y, new_label)
				newnodes = nodes[:]
				for newnodo in newnodes:
					if newnodo.x >= newnode.x:
						newnodo.x = newnodo.x + 1
				newnodes.append(newnode)
				yield newnodes

		elif rule == UNDER:	
			if nodo.x == old_node.x and nodo.y <= old_node.y:	
				newnode = Node(nodo.x, nodo.y-1, new_label)
				newnodes = nodes[:]
				for newnodo in newnodes:
					if newnodo.y <= newnode.y:
						newnodo.y = newnodo.y - 1
				newnodes.append(newnode)
				yield newnodes
		
		elif rule == OVER:
			if nodo.x == old_node.x and nodo.y >= old_node.y:	
				newnode = Node(nodo.x, nodo.y+1, new_label)
				newnodes = nodes[:]
				for newnodo in newnodes:
					if newnodo.y >= newnode.x:
						newnodo.y = newnodo.y + 1
				newnodes.append(newnode)
				yield newnodes
	
def main():
	nodes = []
	nodes.append(Node(0,0,'A'))
	print nodes[0]
	plans = []
	
	for next_plan in genChildren(nodes, 'B', LEFT, 'A'):
		plans.append(next_plan)
		print "A plan:"
		for node in next_plan:
			print(node)
		print "-----"
			
	for plan in plans:
		for next_plan in genChildren(plan, 'C', OVER, 'A'):
			print "A plan:"
			for node in next_plan:
				print(node)
			print "-----"

			
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
	


def filter(plan, label1, rule, label2):
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
	