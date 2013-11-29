from JR_dragger_class import *
from JR_attribute_class import *
from JR_selection_class import *
from JR_material_class import *
import JR_camera_shake
import JR_playblast_tool
import JR_rename_tool
import JR_camera_shuffle
#
class Tools(Selection, DraggerTool, Attributes, Materials):
	def __init__(self):
		Selection.__init__(self)
	def convertSelection(self, toType):
		if toType == 'face':
			return cmds.polyListComponentConversion( self.getSelection(), internal = True, toFace = True )
		elif toType == 'edge':
			return cmds.polyListComponentConversion( self.getSelection(), internal = True, toEdge = True )
		elif toType == 'edgeBorder':
			return cmds.polyListComponentConversion( self.getSelection(), internal = False, toEdge = True )
		elif toType == 'vertex':
			return cmds.polyListComponentConversion( self.getSelection(), toVertex = True )
	def selectionMask(self, toType):
		if cmds.selectMode( query = 1, component = True):
			cmds.selectType( allComponents = False )
			if toType == 'face':
				cmds.selectType(polymeshFace = True)
			elif toType == 'edge':
				cmds.selectType(polymeshEdge = True)
			elif toType == 'vertex':
				cmds.selectType(polymeshVertex = True)
			else:
				cmds.selectType(polymeshFace = True) # default in case no type matches
		else:
			cmds.selectType( allComponents = False, allObjects = True )
	def cameraShakeTool(self):
		JR_camera_shake.CameraShake.toggle()
	def renameTool(self):
		JR_rename_tool.UI()
	def bridgeTool(self):
		X = self.getSelection()
		cmds.polyBridgeEdge(X, ch= 1, divisions= 0, smoothingAngle = 30)
		Attribute.setAttributes( attrs = [ ('Twist', '.twist') , ('Divisions', '.divisions'), ('CurveType', '.curveType'), ('Taper', '.taper') ]  )
		Dragger( X , 'Bridge')
	def playblastTool(self, formatInfo):
		selectedCams = []
		#formatInfo = [ 'qt', 'Sorenson Video 3', [1280, 720] ]
		if self.getSelection == 'None':
			JR_playblast_tool.playblastStart( self.getCameras('scene'), self.desktop, formatInfo )
		else:
			selection = self.getSelection()
			for i in range(len( selection )):
				if self.getType(i)[0] == 'camera':
					selectedCams.append(selection[i])
			if len(selectedCams) == 0:
				print self.desktop
				JR_playblast_tool.playblastStart( self.getCameras('scene') , self.desktop, formatInfo )
			else:
				JR_playblast_tool.playblastStart( selectedCams , self.desktop, formatInfo )
	def extrudeTool(self):
		X = self.getSelection() # adds selection to a variable so we can deselect it later while still using it for the Dragger command.
		if self.getType(0) == 'face':
			cmds.polyExtrudeFacet( X, constructionHistory = 1, keepFacesTogether = 1)
			Attribute.setAttributes( attrs = [('Z Translate', '.localTranslateZ'), ('Local Scale', '.localScale'), ('Division', '.divisions')] )
		elif self.getType(0) == 'edge':
			cmds.polyExtrudeEdge( X, constructionHistory = 1, keepFacesTogether = 1)
			Attribute.setAttributes( attrs = [('Z Translate', '.localTranslateZ'), ('Local Scale', '.localScale'), ('Division', '.divisions')] )
		else:
			pass
		#cmds.select( deselect = 1 ) # removes selection from the face initially extruded, to allow for rotation and translation of new extruded face
		Dragger( X , 'Extrude')
	def chipFacesTool(self):
		# cuts faces off of the poly and then seperates the faces to it's own polygon object, also ungroups them
		selectedFaces = self.getSelection()
		selectionParent = cmds.listRelatives(selectedFaces[0], p=True)
		cmds.polyChipOff( selectedFaces, dup=True)
		seperated = cmds.polySeparate(selectionParent[0])
		allSeperated = [i for i in seperated if 'Separate' not in i]
		if len(allSeperated) > 2:
			cmds.polyUnite(allSeperated[1:])
			new = self.getSelection()
		else:
			new = allSeperated[1]
		old = []; old.append(allSeperated[0])
		oldParent = cmds.listRelatives(old[0], p=True)
		oldParentChildren = cmds.listRelatives(oldParent[0], c=True)
		oldNodesToDelete = set(old) ^ set(oldParentChildren)
		cmds.ungroup( oldParent )
		cmds.delete(new, ch=1)
		cmds.delete(old, ch=1)
		cmds.rename(old, oldParent )
		cmds.select(new)
		self.assignRandomMaterial() # assigns random lambert to newly created poly
		cmds.delete(selectedFaces)
		cmds.select(new) # reselect it after material assign
		JR_rename_tool.UI('exit') # to rename the freshly branched poly
	def bevelTool(self):
		X = self.getSelection() # this is added because once the bevel is performed the face is deselected.
		cmds.polyBevel( X, ch=1, offset=0.5 ,segments =1, smoothingAngle = 30, offsetAsFraction = 1, autoFit = 1, worldSpace = 1, angleTolerance = 180, miteringAngle = 180, uvAssignment = 0, mergeVertices = 1, mergeVertexTolerance = 0.0001 )
		Attribute.setAttributes( attrs = [ ('Offset', '.offset'), ('Segments', '.segments') ] )
		Dragger( X , 'Bevel')
	def polySeperateTool(self):
		cmds.polySeparate()
		cmds.delete(ch=1)
		A = self.getSelection()
		B = cmds.listRelatives(A[0], p=True)
		cmds.ungroup( B )
		cmds.select(A)
		JR_rename_tool.UI('exit') # to rename the freshly branched poly
	def polyMergeTool(self):
		cmds.polyUnite( self.getSelection() )
		cmds.delete(ch=1)
		JR_rename_tool.UI('exit') # to rename the freshly branched poly
	def vertexMergeTool(self):
		length = len( self.getSelection() )
		if self.getSelection() == 'None': # set tool to the merge vertex tool if no verts are selected
			cmds.setToolTo('polyMergeVertexContext')
		else: # if verts are already selected, then run the commands below
			if self.getType(0) == 'vertex': # check to see if the selection is of the vertex type, in case the mask is set to vert but the sel is edge etc.
				if length == 2:
					cmds.polyMergeVertex(alwaysMergeTwoVertices = True)
				elif length  > 2:
					cmds.polyMergeVertex(distance = 0.01)
					newLength = len(self.getSelection())
					if newLength == length: # Nothing was merged because the before and after are the same, state so
						cmds.headsUpMessage( str(length) + ' Verts Selected - 0 Merged', verticalOffset=-100, horizontalOffset=-200 )
					else: # means a merge did happen, so tell how many were merged and how many are left now
						cmds.headsUpMessage( 'FROM ' + str(length) + ' TO ' + str(newLength), verticalOffset=-100, horizontalOffset=-200 )
			else:
				cmds.warning('Vertex not selected')
	def exportTool(self, category):
		if category == 'frostbite':
			cmds.warning( 'here is where the Frostbite export will go')
		Attribute.setAttributes()
	def cameraTool(self, category = 'NA'):
		if category == 'frostbite':
			frostbiteCam = cmds.camera(dr = 1, dgm = 1, ncp = .1, fcp = 10000 )
			cmds.addAttr( frostbiteCam [0], longName = 'isCamera', attributeType = 'bool' )
			cmds.setAttr( str(frostbiteCam [0]) + '.horizontalFilmAperture',  1.4173228346472 )
			cmds.setAttr( str(frostbiteCam [0]) + '.verticalFilmAperture', 0.79724409448905 )
			cmds.setAttr( str(frostbiteCam [0]) + ".isCamera", True )
			cmds.addAttr( longName = 'animPath', dataType = 'string' )
			cmds.setAttr( str(frostbiteCam [0]) + ".animPath" , type = 'string' )
			cmds.addAttr( frostbiteCam [0], longName = 'FOV' )
			cmds.setAttr( str(frostbiteCam [0]) +'.FOV', keyable = True )
			cmds.color( frostbiteCam[0], ud=2 )
		elif category == 'NA':
			cmds.camera(dr = 1, dgm = 1, ncp = .01, fcp = 10000 )
		Attribute.setAttributes()
	def motionPathTool(self, status):
		if status == 'On':
			for i in x:
				a = cmds.snapshot ( i, motionTrail = 1, increment = 1, startTime = cmds.playbackOptions( query = 1, minTime = 1 ), endTime = cmds.playbackOptions( query = 1, maxTime = 1 ) )
				cmds.setAttr( str(a[0]) + '.showFrames', 1)
		if status == 'Off':
			print 'need to fix'
	def sceneCamSwitch(self):
		i = self.getCameras('scene')
		# check cached offset to see if it's beyond the limit
		if Cache.camSceneOffset > len(i) - 1:
			Cache.camSceneOffset = 0
		# create window & script job
		JR_camera_shuffle.createWindow(i) 
		#
		if Cache.cameraJob == 2000: ### this is the default number setup in Cache, not the most ideal way to work :S
			Cache.cameraJob = cmds.scriptJob ( event = ["SelectionChanged", "JR_camera_shuffle.currentCamera()"] ) #, protected=True)
			print Cache.cameraJob, ' this is the camera job #'
		# add to the offset
		Cache.camSceneOffset +=1
		# clear attributes
		#Attribute.setAttributes()
	def defaultCamSwitch(self):
		i = self.getCameras('default')
		# check cached offset to see if it's beyond the limit
		x = cmds.window('cameraWindow', query=True, exists = 1)
		if x is False:
			cmds.scriptJob( kill= int(Cache.cameraJob), force=True)
			print Cache.cameraJob, ' The camera job has been reset'
			Cache.cameraJob = 2000
		if Cache.camDefaultOffset > len(i) - 1:
			Cache.camDefaultOffset = 0
		# switch to the next default camera in the list
		cmds.modelEditor( 'modelPanel4', edit=True, camera = i[ Cache.camDefaultOffset ])
		Cache.camDefaultOffset +=1
		# clear attributes
		#Attribute.setAttributes()
	def selectTool(self):
		selectAttributes = [ ('Normal', 'options = 4'), ('Reflection', '.options = 4') ]
		paintAttributes = [ ('Select', 'options = 4'), ('Soft Select', '.options = 4'), ('Brush Size', '.options = 4') ]
		try:
			if Cache.keyOffset == 0:
				cmds.selectContext('mySelect', edit = True)
				Cache.currentContext = 'mySelect'
				Attribute.setAttributes ( selectAttributes )
			else:
				cmds.artSelectCtx('myPaintSelect', edit = True)
				Cache.currentContext = 'myPaintSelect'
				Attribute.setAttributes ( paintAttributes )
		except:
			if Cache.keyOffset == 0:
				cmds.selectContext ( 'mySelect' )
				Cache.currentContext = 'mySelect'
				Attribute.setAttributes ( selectAttributes )
			else:
				cmds.artSelectCtx ( 'myPaintSelect' )
				Cache.currentContext = 'myPaintSelect'
				Attribute.setAttributes ( paintAttributes )
		cmds.setToolTo( Cache.currentContext )
	def moveTool(self):
		try:
			if Cache.keyOffset == 0:
				cmds.manipMoveContext('myMove', edit = True, mode = 2 ) # world mode
				Cache.currentContext = 'myMove'
				Attribute.setAttributes()
			else:
				cmds.manipMoveContext('myMove', edit = True, mode = 0 ) # object mode
				Cache.currentContext = 'myMove'
				Attribute.setAttributes()
		except:
			if Cache.keyOffset == 0:
				cmds.manipMoveContext( 'myMove', mode = 2 ) # world mode
				Cache.currentContext = 'myMove'
				Attribute.setAttributes()
			else:
				cmds.manipMoveContext('myMove', mode = 0 ) # object mode
				Cache.currentContext = 'myMove'
				Attribute.setAttributes()
		cmds.setToolTo( Cache.currentContext )
	def rotateTool(self):
		try:
			if Cache.keyOffset == 0:
				cmds.manipRotateContext('myRotate', edit = True, mode = 0) # world mode
				Cache.currentContext = 'myRotate'
				Attribute.setAttributes()
			else:
				cmds.manipRotateContext('myRotate', edit = True, mode = 1) # local mode
				Cache.currentContext = 'myRotate'
				Attribute.setAttributes()
		except:
			if Cache.keyOffset == 0:
				cmds.manipRotateContext( 'myRotate', mode = 0 ) # world mode
				Cache.currentContext = 'myRotate'
				Attribute.setAttributes()
			else:
				cmds.manipRotateContext('myRotate', mode = 1 ) # local mode
				Cache.currentContext = 'myRotate'
				Attribute.setAttributes()
		cmds.setToolTo( Cache.currentContext )
	def scaleTool(self):
		try:
			if Cache.keyOffset == 0:
				cmds.manipScaleContext('myScale', edit = True, mode = 2) # world mode
				Cache.currentContext = 'myScale'
				Attribute.setAttributes()
			else:
				cmds.manipScaleContext('myScale', edit = True, mode = 0) # object mode
				Cache.currentContext = 'myScale'
				Attribute.setAttributes()
		except:
			if Cache.keyOffset == 0:
				cmds.manipScaleContext( 'myScale', mode = 2 ) # world mode
				Cache.currentContext = 'myScale'
				Attribute.setAttributes()
			else:
				cmds.manipScaleContext('myScale', mode = 0) # object mode
				Cache.currentContext = 'myScale'
				Attribute.setAttributes()
		cmds.setToolTo( Cache.currentContext )
#
Tool = Tools()