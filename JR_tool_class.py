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
	def createInMiddle(self, execCommand):
		Cache.locatorList = []
		if self.getSelection() == 'None':
			location = self.getMiddle()[0]
			exec execCommand
			cmds.xform(t = location)
		else:
			if len(self.getSelection()) == 1:
				location = self.getMiddle()[0]
				exec execCommand
				cmds.xform(t = location)
			else:
				items = []
				for i in self.getSelection():
					Cache.locatorList.append(i) #to understand which locator goes to which selection point
					cmds.select(i)
					location = self.getMiddle()[0]
					exec execCommand
					items.append(cmds.ls(selection=True))
					cmds.xform(t = location)
				cmds.select(clear = 1)
				for i in items:
					cmds.select(i, add = 1)
	def assignMaterialTool(self):
		self.assignRandomMaterial()
	def cameraShakeTool(self):
		JR_camera_shake.run()
	def renameTool(self):
		JR_rename_tool.UI()
	def bridgeTool(self):
		X = self.getSelection()
		cmds.polyBridgeEdge(X, ch= 1, divisions= 0, smoothingAngle = 30)
		Attribute.setAttributes( attrs = [ ('Twist', '.twist') , ('Divisions', '.divisions'), ('CurveType', '.curveType'), ('Taper', '.taper') ]  )
		Dragger( X , 'Bridge')
	def smoothTool(self):
		X = self.getSelection()
		if self.getType(0) == 'face':
			cmds.polySubdivideFacet
			Attribute.setAttributes( attrs = [ ('U', '.divisionsU') , ('V', '.divisionsV') ]  )
		Dragger(X, 'polySubdFace')
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
	def splitFaceTool(self):
		cmds.polySplitCtx('polySplitContext', edit=1, snaptoedge=1, enablesnap=1, precsnap=10 )
		cmds.setToolTo('polySplitContext')
		#cmds.polySplitCtx2('polySplitContext2', edit=1, constrainToEdges=1, edgeMagnets=2, st=0.2 )
		#cmds.setToolTo('polySplitContext2')
		#cmds.polySplitCtx2('cutFaces', constrainToEdges=1, edgeMagnets=1, st=0.1) 
		#cmds.setToolTo('cutFaces')
	def extrudeTool(self):
		X = self.getSelection() # adds selection to a variable so we can deselect it later while still using it for the Dragger command.
		if self.getType(0) == 'face':
			cmds.polyExtrudeFacet( X, constructionHistory = 1, keepFacesTogether = 1)
			Attribute.setAttributes( attrs = [('Thickness', '.thickness'), ('Offset', '.offset'), ('Division', '.divisions'), ('Z Translate', '.localTranslateZ'), ('Faces Together', '.keepFacesTogether')] )
		elif self.getType(0) == 'edge':
			cmds.polyExtrudeEdge( X, constructionHistory = 1, keepFacesTogether = 1)
			Attribute.setAttributes( attrs = [('Thickness', '.thickness'), ('Offset', '.offset'), ('Division', '.divisions'), ('Z Translate', '.localTranslateZ')] )
		else:
			pass
		#cmds.select( deselect = 1 ) # removes selection from the face initially extruded, to allow for rotation and translation of new extruded face
		Dragger( X , 'Extrude')
	def jointTool(self):
		if len(self.getSelection()) == 1:
			location = self.getMiddle()[0]
			cmds.joint(p = location)
		else:
			items = []
			for i in self.getSelection():
				cmds.select(i)
				location = self.getMiddle()[0]
				cmds.joint(p = location)
				items.append(cmds.ls(selection=True))
			cmds.select(clear = 1)
			for i in items:
				cmds.select(i, add = 1)
	def centerPivot(self, item):
		cmds.xform(item, centerPivots = True)
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
		print oldNodesToDelete, ' this is old nodes to delete'
		cmds.ungroup( oldParent )
		cmds.delete(new, ch=1)
		cmds.delete(old, ch=1)
		cmds.rename(old, oldParent )
		cmds.select(new)
		self.assignRandomMaterial() # assigns random lambert to newly created poly
		cmds.delete(selectedFaces)
		cmds.select(old)
		cmds.xform(centerPivots = True)
		cmds.select(new) # reselect it after material assign
		cmds.xform(centerPivots = True) # Center pivot of new article.
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
	def constrainToParent(self, bakeOrNo = 'Bake', maintainOffset = 'No'):
		sl = cmds.ls(selection=True)
		if maintainOffset == 'No':
			cmds.parentConstraint( sl[1], sl[0] )
		elif maintainOffset == 'Maintain':
			cmds.parentConstraint( sl[1], sl[0], mo = True )
		cmds.select(sl[0])
		if bakeOrNo == 'bake':
			start = cmds.findKeyframe( self.getSelection(), which = "first" )
			end = cmds.findKeyframe( self.getSelection(), which = "last" )
			if start == end: # this means there's no keyframes
				start = cmds.playbackOptions(q=1, minTime=1)
				end =   cmds.playbackOptions(q=1, maxTime=1)
			cmds.bakeResults( sl[0],time=(start, end), simulation=True )
			cmds.delete( cn=True )
			if self.getType(0)[0] == 'camera':
				objectChild = cmds.listRelatives( sl[0], c=True )
				# all attributes for camera child node
				cmds.delete( objectChild, at='hfa', c=True )
				cmds.delete( objectChild, at='vfa', c=True )
				cmds.delete( objectChild, at='fl', c=True )
				cmds.delete( objectChild, at='lsr', c=True )
				cmds.delete( objectChild, at='fs', c=True )
				cmds.delete( objectChild, at='fd', c=True )
				cmds.delete( objectChild, at='sa', c=True )
				cmds.delete( objectChild, at='coi', c=True )
				# all attributes for camera node
				cmds.delete( sl[0], at='FOV', c=True )
				cmds.delete( sl[0], at='v', c=True )
				cmds.delete( sl[0], at='sz', c=True )
				cmds.delete( sl[0], at='sy', c=True )
				cmds.delete( sl[0], at='sx', c=True )
				# now initiate export selection
				cmds.ExportSelection()
		else:
			pass
	def exportTool(self, category):
		if category == 'frostbite':
			cmds.warning( 'here is where the Frostbite export will go')
		else:
			if self.getSelection == 'None':
				cmds.Export()
			else:
				cmds.ExportSelection()
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
	def mirrorModelingTool(self, direction, *args):
		original = self.getSelection()
		pivot = cmds.xform(query = True, worldSpace = True, scalePivot = True)
		instance = original[0]+'_instance'
		try:
			if instance:
				cmds.delete(instance)
				cmds.instance(name = instance)
		except:
			cmds.instance(name = instance)
		if direction == '-x':
			cmds.scale(-1,1,1, instance, r=1, )
			position = -1*(pivot[0]*2)
			cmds.move(position, 0, 0, instance, relative=True)
		elif direction == '+x':
			cmds.scale(-1,1,1, instance, r=1, )
			position = 1*(pivot[0]*2)
			cmds.move(position, 0, 0, instance, relative=True)
		elif direction == '-y':
			cmds.scale(1,-1,1, instance, r=1, )
			position = -1*(pivot[1]*2)
			cmds.move(0, position, 0, instance, relative=True)
		elif direction == '+y':
			cmds.scale(1,1,1, instance, r=1, )
			position = 1*(pivot[1]*2)
			cmds.move(0, position, 0, instance, relative=True)
		elif direction == '-z':
			cmds.scale(1,1,-1, instance, r=1, )
			position = -1*(pivot[2]*2)
			cmds.move(0, 0, position, instance, relative=True)
		elif direction == '+z':
			cmds.scale(1,1,1, instance, r=1, )
			position = 1*(pivot[2]*2)
			cmds.move(0, 0, position, instance, relative=True)
		cmds.deleteUI('mirror', window=True )
		#cmds.select(clear = True)
		#cmds.select(new)
		#cmds.createDisplayLayer(name = 'Instances', noRecurse=True)
		#cmds.setAttr('Instances'+'.displayType', 2)
	def creaseTool(self):
		cmds.polyCrease( value=0.9 )
		Attribute.setAttributes( attrs = [ ('Offset', '.offset'), ('Segments', '.segments') ] )
		Dragger( X , 'Bevel')
	def primitiveTool(self):
		if self.getType(0)[1] == 'CAMERA':
			Attribute.setAttributes( attrs = [('Locator Scale', '.locatorScale')] )
			history = ''
		if self.getHistory(self.getSelection(), 0, 'polyCube' ):
			Attribute.setAttributes( attrs = [ ('Width', '.width') , ('Height', '.height'), ('Depth', '.depth'), ('Width Div', '.subdivisionsWidth') , ('Height Div', '.subdivisionsHeight'), ('Depth Div', '.subdivisionsDepth') ]  )
			history = 'polyCube' 
		elif self.getHistory(self.getSelection(), 0, 'polySphere' ):
			Attribute.setAttributes( attrs = [ ('Axis Div', '.subdivisionsAxis') , ('Height Div', '.subdivisionsHeight') ]  )
			history = 'polySphere' 
		elif self.getHistory(self.getSelection(), 0, 'polyCylinder' ):
			Attribute.setAttributes( attrs = [ ('Radius', '.radius') , ('Height', '.height'), ('Axis Div', '.subdivisionsAxis') , ('Height Div', '.subdivisionsHeight'), ('Caps Div', '.subdivisionsCaps') ]  )
			history = 'polyCylinder' 
		elif self.getHistory(self.getSelection(), 0, 'polyTorus' ):
			Attribute.setAttributes( attrs = [ ('Radius', '.radius') , ('Section Radius', '.sectionRadius'), ('Twist', '.twist') , ('Axis Div', '.subdivisionsAxis'), ('Height Div', '.subdivisionsHeight') ]  )
			history = 'polyTorus' 
		elif self.getHistory(self.getSelection(), 0, 'polyCone' ):
			Attribute.setAttributes( attrs = [ ('Radius', '.radius') , ('Height', '.height'), ('Axis Div', '.subdivisionsAxis') , ('Height Div', '.subdivisionsHeight'), ('Cap Div', '.subdivisionsCap') ]  )
			history = 'polyCone' 
		elif self.getHistory(self.getSelection(), 0, 'polyPyramid' ):
			Attribute.setAttributes( attrs = [ ('Radius', '.sideLength') , ('Height Div', '.subdivisionsHeight'), ('Cap Div', '.subdivisionsCaps') , ('Sides', '.numberOfSides') ]  )
			history = 'polyPyramid'
		elif self.getHistory(self.getSelection(), 0, 'polyPipe' ):
			Attribute.setAttributes( attrs = [ ('Radius', '.radius') , ('Round Cap', '.roundCap'),  ('Height', '.height'), ('Thickness', '.thickness') , ('Axis Div', '.subdivisionsAxis'), ('Height Div', '.subdivisionsHeight'), ('Cap Div', '.subdivisionsCaps') ]  )
			history = 'polyPipe'
		elif self.getHistory(self.getSelection(), 0, 'polyPlane' ):
			Attribute.setAttributes( attrs = [ ('Width', '.width') , ('Height', '.height'),  ('Width Div', '.subdivisionsWidth'), ('Height Div', '.subdivisionsHeight') ]  )
			history = 'polyPlane'  
		Dragger(self.getSelection(), history )
	def selectTool(self):
		selectAttributes = [ ('Normal', 'options = 4'), ('Reflection', '.options = 4') ]
		paintAttributes = [ ('Select', 'options = 4'), ('Soft Select', '.options = 4'), ('Brush Size', '.options = 4') ]
		try:
			if Cache.keyOffset == 0:
				cmds.selectContext('mySelect', edit = True)
				Cache.currentContext = 'mySelect'
				Attribute.setAttributes ( selectAttributes )
			elif Cache.keyOffset == 1:
				cmds.artSelectCtx('myPaintSelect', edit = True)
				Cache.currentContext = 'myPaintSelect'
				Attribute.setAttributes ( paintAttributes )
			elif Cache.keyOffset == 2:
				Cache.currentContext = 'selectDragger'
				self.primitiveTool()
		except:
			if Cache.keyOffset == 0:
				cmds.selectContext ( 'mySelect' )
				Cache.currentContext = 'mySelect'
				Attribute.setAttributes ( selectAttributes )
			elif Cache.keyOffset == 1:
				cmds.artSelectCtx ( 'myPaintSelect' )
				Cache.currentContext = 'myPaintSelect'
				Attribute.setAttributes ( paintAttributes )
			elif Cache.keyOffset == 2:
				Cache.currentContext = 'selectDragger'
				self.primitiveTool()
		if Cache.currentContext != 'selectDragger':
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