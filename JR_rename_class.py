from JR_selection_class import *
class Rename(Selection):
	def __init__(self, selection, name):
		self.name = name
		self.selection = selection + name # append the name to the end of the selection list so we can process it's properties with a -1 call in the 'i'
	def processNamespace(self, i):
		if self.selection[-1][0] == ':': # if the input name starts with : then we want to return the root
			return ':'
		elif len( self.getNamespace(-1) ) >= 2: # if it is longer than 1, means it isn't the root and thus we want to return it's namespace
			return self.getNamespace(-1)
		else:
			return self.getNamespace(i) # if none of the above then there is no namespace in the input name and we want to return the selection namespace.
	def processRename(self, i):
		if self.selection[-1][0] == '_': # Suffix addition only
			return ( self.getAfterNamespace(i) + self.selection[-1] )
		elif self.selection[-1][-1] == '_': # Prefix addition only
			return ( self.selection[-1] + self.getAfterNamespace(i) )
		if self.selection[-1][-1] == ':': # Namespace replacement only
			if self.getIteratorValue(i) == 1: # value of 1 means no iterator present in original name
				return self.getPrefix(i) 
			else:
				return ( self.getPrefix(i) +  self.getIteratorValue(i) + self.getSuffix(i) )
		else:
			if self.getIteratorValue(-1) == 1: # value of 1 means no iterator present in original name
				if len(self.selection) > 2: # for more than one item selected
					return ( self.getPrefix(-1) + '_' + str((int( self.getIteratorValue(-1) ) + int(i)))  )
				else: #for only one item selected
					return self.getPrefix(-1) 
			else:
				if len(self.selection) > 2: # for more than one item selected
					return ( self.getPrefix(-1) + str( ( int( self.getIteratorValue(-1) ) + int(i) ) ) + self.getSuffix(-1) )
				else: #for only one item selected
					return self.getPrefix(-1)