import re
import os
import maya.cmds as cmds
class Selection():
	def __init__(self):
		### establishing user paths to use in scripts
		userPath = os.path.expanduser("~")
		self.userFolder = os.path.dirname(userPath)
		#
		self.desktop = self.userFolder + '/Desktop/'
	def getParent(self, i):
		return cmds.listRelatives(i, p=True)
	def getSelection(self):
		initialSelection = cmds.ls(orderedSelection=True, flatten=True)
		if initialSelection == []:
			return 'None'
		else:
			return sorted(initialSelection)
	def getCameras(self, camType):
		cameraScene = []
		cameraDefault = ['perspShape', 'sideShape', 'topShape', 'frontShape']
		cameraAll = cmds.ls(cameras = True)
		if len(cameraAll) == len(cameraDefault) :
			print ' all is equal to default'
		else:
			cameraShape = sorted(list( set(cameraAll) - set(cameraDefault) ) )
			cameraScene =  cmds.listRelatives( cameraShape, allParents=True )
		if camType == 'default':
			return cameraDefault
		elif camType == 'scene':	
			return cameraScene
	def getPanel(self, panelName):
		x = [i for i in cmds.getPanel(vis=True) if panelName in i]
		return x
	def getContext(self):
		return cmds.currentCtx()
	def getMiddle(self):
		# so far this method is only giving values for the position, if you want to put in values
		# for the rotation and normal directino you'll have to devise actions for those in here as well
		# using the 1 and 2 slots in the middle attr.
		middle = [ [0,0,0], [0,0,0], [0,0,0] ] # 0 is the position, 1 is the rotation, 2 is the normal Angle
		if self.getSelection() == 'None':
			middle[0] = [0,0,0]
		elif len(self.getSelection() ) == 1: # use this if only 1 objects selected
			#cmds.select(self.getSelection())
			bbx = cmds.xform(q=True, bb=True, ws=True) # world space
			middle[0] = [ ((bbx[0] + bbx[3]) / 2.0), ((bbx[1] + bbx[4]) / 2.0), ((bbx[2] + bbx[5]) / 2.0) ]
			#middle[0] = cmds.xform(self.getSelection(), query = 1, translation = 1)
		    #middle[0] = cmds.objectCenter(self.getSelection() ) # find the center of the object and use that as the middle
		else: # means more than one item is in the selection list
		    for i in self.getSelection():
		    	bbx = cmds.xform(i, q=True, bb=True, ws=True) # world space
		    	bbf = [ ((bbx[0] + bbx[3]) / 2.0), ((bbx[1] + bbx[4]) / 2.0), ((bbx[2] + bbx[5]) / 2.0) ]
		    	middle[0] = [x + y for x, y in zip(bbf, middle[0])] # sum of the lists of middle and then the object center
		        #middle[0] = [x + y for x, y in zip(cmds.objectCenter(i), middle[0])] # sum of the lists of middle and then the object center
		    middle[0] =[x / len(self.getSelection() ) for x in middle[0] ] # average out the x,y,z values for the final middle list
		return middle
	def getType(self, i):
		currentSelection = self.getSelection()
		if currentSelection != 'None':
			if 'e[' in currentSelection[i]:
				return 'edge'
			elif 'vtx[' in currentSelection[i]:
				return 'vertex'
			elif 'f[' in currentSelection[i]:
				return 'face'
			elif 'map[' in currentSelection[i]:
				return 'uv'
			elif 'vtxFace[' in currentSelection[i]:
				return 'vtxFace'
			elif 'cv[' in currentSelection[i]:
				return 'controlVertex'
			elif 'sf[' in currentSelection[i]:
				return 'surfacePath'
			elif 'uv[' in currentSelection[i]:
				return 'surfacePoint'
			else:
				if cmds.objectType( currentSelection[i] ) == 'transform':
					#print 'it is a transform'
					getParent = cmds.listRelatives(currentSelection[i], s=True)
					checkType = cmds.objectType( getParent[0] )
					print checkType, '  this is the raw type in the transform section'
					if checkType == 'mesh':
						return 'mesh'
					elif checkType == 'camera':
						return 'camera', 'CAMERA'
					elif checkType == 'spotLight':
						return 'spotLight', 'LIGHT'
					elif checkType == 'directionalLight':
						return 'directionalLight', 'LIGHT'
					elif checkType == 'pointLight':
						return 'pointLight', 'LIGHT'
					elif checkType == 'ambientLight':
						return 'ambientLight', 'LIGHT'
					elif checkType == 'areaLight':
						return 'areaLight', 'LIGHT'
					elif checkType == 'volumeLight':
						return 'volumeLight', 'LIGHT'
					elif checkType == 'nurbsSurface':
						return 'nurb'
					elif checkType == 'nurbsCurve':
						return 'curve'
					elif checkType == 'locator':
						return 'locator'
				elif cmds.objectType( currentSelection[i] ) == 'joint':
					return 'joint'
		else:
			return 'None'
	def getHistory(self, selection, i, historyName):
		self.selection = selection
		if self.getType(0) == 'joint' or self.getType(0) == 'mesh': # need this because joints can be placed underneath parent geo and then the radius gets adjusted through them. 
			selectionParent = self.selection
		elif i == '':
			selectionParent = cmds.listRelatives(self.selection, p=True) # creates a list for the selection parnet var
		else:
			selectionParent = cmds.listRelatives(self.selection[i], p=True) # creates a list for the selection parnet var
		if selectionParent == None:
			selectionParent = self.selection # already a list so no need to have a [0] callout in it
		if historyName == 'Extrude':
			if self.getType(0) == 'vert':
				historyName = 'polyExtrudeVertex'
			elif self.getType(0) == 'edge':
				historyName = 'polyExtrudeEdge'
			elif self.getType(0) == 'face':
				historyName = 'polyExtrudeFace'
		elif historyName == 'Bevel':
			historyName = 'polyBevel'
		historyList = cmds.listHistory( str(selectionParent[0]) ) # need the [0] because selection parent is always a list no matter what.
		return sorted( set(x for x in historyList if historyName in x) )
	def reFunction(self, item, isolate):
		# This method finds the location of 
		# the provided isolate var in the 
		# provided item var and returns a list
		#
		s = re.compile( isolate ) # compile a string obj, ie: '\:' or '\d+'
		f = s.finditer(item)
		return [ x.span() for x in f ]
	def getIteratorLocation(self, i):
		# This method uses the reFunction to
		# find the location of a selections
		# iter if there is digits in the selection
		#
		digitList = [x for x in self.selection[i] if x.isdigit()]
		if digitList == []:
			return []
		else:
			return ( self.reFunction (self.selection[i] , '\d+') ) 
	def getIteratorValue(self, i):
		# This method process the list from
		# getIteratorLocation and returns the value of
		# last nuber group in the selected object
		#
		iterLocation = self.getIteratorLocation(i)
		if iterLocation == []:
			return 1
		else:
			return self.selection[i] [ iterLocation [-1][0] : iterLocation [-1][1] ]
	def getPrefix(self, i):
		# This method uses the getIterLocation (if there is one)
		# and the getNamespace value, if there is one, to identify
		# the value of the prefix which will be between both items
		#
		iterLocation = self.getIteratorLocation(i)
		if self.getNamespace(i) == ':':
			if iterLocation == []:
				return self.selection[i]
			else:
				prefix = self.selection[i] [ : iterLocation[-1][0] ]
				return prefix
		else:
			if iterLocation == []:
				return self.selection[i] [ len(self.getNamespace(i)) : ] # + 1 : ]
			else:
				prefix = self.selection[i] [ : iterLocation[-1][0] ]
				return prefix[len(self.getNamespace(i)) :] # + 1 :]
	def getSuffix(self, i):
		iterLocation = self.getIteratorLocation(i)
		if iterLocation == []:
			return ''
		else:
			suffix = self.selection[i] [ iterLocation[-1][1] : ]
			return suffix
	def getNamespace(self, i):
		if ':' in self.selection[i]:
			V = self.reFunction(self.selection[i], '\:+')
			return self.selection[i] [ : V[0][1] ]
		else: # no namespaces present
			return ':'
	def getAfterNamespace(self, i):
		if ':' in self.selection[i]:
			V = self.reFunction(self.selection[i], '\:+')
			return self.selection[i] [ V[0][1] : ]
		else: # no namespaces present
			return self.selection[i]