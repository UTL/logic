from collections import deque
from random import shuffle
import time

FILENAME = "result.log"

class Node(object):
	def __init__(self, l, s, r, depth):
		self.l = l #left track
		self.r = r #right track
		self.s = s #siding track
		self.parent = None
		self.depth = depth
		self.myhash = None
		
	def getTuple(self):
		return (self.l,self.s,self.r)
	
	def setParent(self, parent):
		self.parent = parent
		
	def __eq__(self, other): 
		return self.l == other.l and self.r == other.r and self.s == other.s

	def __str__(self):
		return str((self.l,self.s,self.r))
		
	def __repr__(self):
		return str((self.l,self.s,self.r))
	
	def __hash__(self):
		if self.myhash != None:
			return self.myhash
		self.myhash = hash(''.join(self.l)+','+''.join(self.s)+','+''.join(self.r))	
		return self.myhash
		
	def human_readable(self):
		return  "--------"+str(self.depth +1)+"---------\n" + ''.join(self.l) + " ==>\t<== " + ''.join(reversed(self.r)) +"\n\t<== " +''.join(reversed(self.s)) 

	def linear_repr(self):
		return "["+''.join(self.l)+','+''.join(reversed(self.s))+','+''.join(reversed(self.r))+"]"
	
