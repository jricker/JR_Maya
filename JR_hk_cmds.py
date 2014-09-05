from JR_cache_class import *
import JR_custom_window
from JR_hud_class import HUDs
from JR_tool_class import Tools
from JR_attribute_class import Attributes
from JR_selection_class import Selection
from JR_refresh_modules import Refresh
from JR_material_class import Materials
import maya.mel as mel
import maya.cmds as cmds
class Hotkeys(Selection, Tools, Attributes, Materials, HUDs, Refresh ):
	def __init__(self):
		Selection.__init__(self)
		Attributes.__init__(self)
		Tools.__init__(self)
		Materials.__init__(self)
		HUDs.__init__(self)
	def tilde(self):
		self.attr_toggleUp()
	def alt_tilde(self):
		self.attr_toggleDown()
	def ctrl_tilde(self):
		self.displayMenu()
	###############################################      1      ###############################################
	def one(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			self.selectionMask( 'vertex' )
		else: # select mode is set to component
			if self.getType(0) == 'face' or self.getType(0) == 'edge': 
			# Check to see if another component is alread selected
			# This will switch the selection over
				cmds.select(self.convertSelection('vertex'))
				self.selectionMask( 'vertex' )
			else:
				if cmds.selectType( query = 1, polymeshVertex = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					self.selectionMask( 'vertex' )
	def alt_one(self):
		JR_custom_window.outlinerWindow()
	def shift_one(self):
		Cache.subdivisionLevel = '1'
		mel.eval('setDisplaySmoothness 1;')
		cmds.subdivDisplaySmoothness( s=1 )
	###############################################      2      ###############################################
	def two(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			self.selectionMask( 'edge' )
		else: # select mode is set to component
			if self.getType(0) == 'face':
				cmds.select(self.convertSelection('edge'))
				self.selectionMask( 'edge' )
			elif self.getType(0) == 'vertex':
				cmds.select(self.convertSelection('edgeBorder'))
				self.selectionMask( 'edge' )
			else:
				if cmds.selectType( query = 1, polymeshEdge = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					self.selectionMask( 'edge' )
	def alt_two(self):
		JR_custom_window.hyperWindow()
	def shift_two(self):
		Cache.subdivisionLevel = '2'
		mel.eval('setDisplaySmoothness 2;')
		cmds.subdivDisplaySmoothness( s=2 )
	###############################################      3      ###############################################
	def three(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			self.selectionMask( 'face' )
		else: # select mode is set to component
			if self.getType(0) == 'vertex' or self.getType(0) == 'edge':
				cmds.select(self.convertSelection('face'))
				self.selectionMask( 'face' )
			else:
				if cmds.selectType( query = 1, polymeshFace = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					self.selectionMask( 'face' )
	def alt_three(self):
		JR_custom_window.graphWindow()
	def shift_three(self):
		Cache.subdivisionLevel = '3'
		mel.eval('setDisplaySmoothness 3;')
		cmds.subdivDisplaySmoothness( s=3 )
	###############################################      4      ###############################################
	def alt_four(self):
		cmds.HypershadeWindow()
	###############################################      5      ###############################################
	def alt_five(self):
		mel.eval('tearOffPanel "UV Texture Editor" "polyTexturePlacementPanel" true;')
	###############################################      G      ###############################################
	def alt_g(self):
		cmds.ToggleGrid()
	###############################################      Q      ###############################################
	def q (self):
		offsetCount = 2
		if self.getContext() == 'mySelect' or self.getContext() == 'myPaintSelect' or Cache.currentContext == 'selectDragger':
			if Cache.keyOffset >= offsetCount-1:
				Cache.keyOffset = 0
			else:
				Cache.keyOffset += 1
		else:
			Cache.keyOffset = 0
		if Cache.keyOffset == 0:
			Cache.currentTool = 'select - normal'
		elif Cache.keyOffset == 1:
			Cache.currentTool = 'select - paint'
		self.selectTool()
	def q_release(self):
		print 'claiming "q" release from default maya'
		self.updateToolHUD()
	def alt_q(self):
		Cache.keyOffset = 2
		Cache.currentTool = 'select - attrs'
		if self.getType(0) == 'joint':
			mel.eval('jdsWin;') # shows the joint size window for all joints
		else:
			self.selectTool()
		self.updateToolHUD()
	###############################################      W      ###############################################
	def w (self):
		offsetCount = 2
		if self.getContext() == 'myMove':
			if Cache.keyOffset >= offsetCount - 1:
				Cache.keyOffset = 0
			else:
				Cache.keyOffset += 1
		else:
			Cache.keyOffset = 0
		if Cache.keyOffset == 0:
			Cache.currentTool = 'move - world'
		elif Cache.keyOffset == 1:
			Cache.currentTool = 'move - local'
		self.moveTool()
	def w_release(self):
		print 'claiming "w" release from default maya'
		self.updateToolHUD()
	###############################################      E      ###############################################
	def e (self):
		offsetCount = 2
		if self.getContext() == 'myRotate':
			if Cache.keyOffset >= offsetCount - 1:
				Cache.keyOffset = 0
			else:
				Cache.keyOffset += 1
		else:
			Cache.keyOffset = 0
		if Cache.keyOffset == 0:
			Cache.currentTool = 'rotate - local'
		elif Cache.keyOffset == 1:
			Cache.currentTool = 'rotate - world'
		self.rotateTool()
	def e_release(self):
		print 'claiming "e" release from default maya'
		self.updateToolHUD()
	def ctrl_e(self):
		self.exportTool(Cache.currentCategory)
		self.updateToolHUD()
	def alt_e(self):
		if Cache.currentCategory == 'frostbite':
			Cache.currentTool = 'Importing Assets'
			self.exportTool(Cache.currentCategory)
		else:
			Cache.currentTool = ''
			cmds.warning(' only works with Frostbite category right now')
		self.updateToolHUD()
	###############################################      R      ###############################################
	def r (self):
		offsetCount = 2
		if self.getContext() == 'myScale':
			if Cache.keyOffset >= offsetCount - 1:
				Cache.keyOffset = 0
			else:
				Cache.keyOffset += 1
		else:
			Cache.keyOffset = 0
		if Cache.keyOffset == 0:
			Cache.currentTool = 'scale - world'
		elif Cache.keyOffset == 1:
			Cache.currentTool = 'scale - local'
		self.scaleTool()
	def R (self):
		self.refreshAllClasses()
		cmds.warning('All Modules Refreshed :)')
	def r_release(self):
		print 'claiming "r" release from default maya'
		self.updateToolHUD()
	def alt_r(self):
		self.renameTool()
		self.updateToolHUD()
	def ctrl_r(self):
		cmds.ReferenceEditor()
	###############################################      L      ###############################################
	def ctrl_l (self):
		X = self.getSelection()
		self.createInMiddle("cmds.spaceLocator( name = 'JR_locator_01', position = (0,0,0) )")
		if Cache.locatorList != []:
			newLocators = self.getSelection()
			#print Cache.locatorList, ' this is the cache list'
			#print self.getSelection(), 'this is the locator list'
			# automatically bake the locators if more than one has been created, because I would only create more than one if it was necessary for verts of faces.
			#parentObject = self.getParent(Cache.locatorList[0] )
			parentObject = self.getParent(X)
			#print parentObject[0]
			start = cmds.findKeyframe( parentObject, which = "first" )
			end = cmds.findKeyframe( parentObject, which = "last" )
			if start == end: # this means there's no keyframes
				start = cmds.playbackOptions(q=1, minTime=1)
				end =   cmds.playbackOptions(q=1, maxTime=1)
			print end-start, ' this is end - start value'
			print start, ' THIS IS START'
			for i in range(int(end-start)):
				print i, ' this is the iterator value'
				cmds.currentTime(start)
				for x in range(len(Cache.locatorList)):
					cmds.select(Cache.locatorList[x])
					print Cache.locatorList[x], ' this is the locator list for x'
					print newLocators[x], ' this is the new locators for x'
					middle =  self.getMiddle()
					cmds.xform(newLocators[x], t= middle[0])
					cmds.setKeyframe(newLocators[x])
					#print cache.locatorList[i], ' pared with ...', self.getSelection(i)
				start += 1
			print 'finished'
		else:
			print 'not working'
	###############################################      P      ###############################################
	def alt_p (self):
		self.playblastHUD()
	def ctrl_p(self):
		if self.getType(0) == 'face' or self.getType(0) == 'mesh':
			print ' not sure which tool should go here .. '
	###############################################      F      ###############################################
	def F (self):
		# Sets a Keyframe on the focal length of a camera if selected - Just like Shift + w sets a keyframe on the move attr
		if self.getType(0)[1] == 'CAMERA':
			currentCamera = self.getSelection()
			cmds.setKeyframe(str(currentCamera[0]) + '.fl')
		if self.getType(0) == 'edge':
			cmds.polyCloseBorder()
		if self.getType(0) == 'vertex':
			self.flattenVertex()
	###############################################      M      ###############################################
	def ctrl_m(self):
		self.mirrorMenu( self.mirrorModelingTool )
	def ctrl_M(self):
		for i in self.getSelection():
			self.assignRandomMaterial(item=i)	
	def m(self):
		self.assignMaterialTool()
	def M(self):
		self.assignTestMaterial()
	###############################################      B      ###############################################
	def alt_b(self):
		if self.getSelection() == 'None':
			cmds.CycleBackgroundColor() # cycles the background color as per the default
		else:
			if self.getType(0) == 'face' or self.getType(0) == 'vertex' or self.getType(0) == 'edge':
				self.bevelTool()
			# switch this over to recognize the animation category later on istead of just fitting to a camera selection. Should be able to work on any object selected
			else:
				start = cmds.findKeyframe( self.getSelection(), which = "first" )
				end = cmds.findKeyframe( self.getSelection(), which = "last" )
				if start == end: # this means there's no keyframes
					start = cmds.playbackOptions(q=1, minTime=1)
					end =   cmds.playbackOptions(q=1, maxTime=1)
				cmds.bakeResults(self.getSelection(), simulation = True, time =(start,end), sampleBy = 1 )

	###############################################      D      ###############################################
	def d (self):
		# Tool To create the measurement tool when vertexes are selected
		if self.getType(0) == 'vertex':
			locators = cmds.ls(type = 'locator')
			distances = cmds.ls(type = 'distanceDimShape')
			cmds.distanceDimension(startPoint = cmds.pointPosition( self.getSelection()[0]) ,endPoint= cmds.pointPosition( self.getSelection()[1] ))
			newLocators = set(cmds.ls(type='locator')) - set(locators)
			newDistances = set(cmds.ls(type='distanceDimShape')) - set(distances)
			if len(newLocators) == 2:
			    cmds.group(list(newLocators)[0], list(newLocators)[1] , list(newDistances)[0], n = 'measurement')
			elif len(newLocators) == 1:
			    cmds.group(list(newLocators)[0], list(newDistances)[0], n = 'measurement')
		elif self.getType(0) == 'face':
			cmds.polySubdivideFacet(sbm=1) #starts it off in linear form
			self.smoothTool()
		##elif self.getType(0) == 'mesh':
		##	self.smoothTool()
		self.updateToolHUD()
	def alt_d (self):
		cmds.xform(cp=1)
	###############################################      I      ###############################################
	def i (self):
		if self.getSelection() != 'None':
			mel.eval('polyCleanupArgList 3 { "0","2","1","0","1","1","1","0","0","1e-005","0","1e-005","0","1e-005","0","-1","0" }')
		else:
			cmds.playbackOptions( minTime = cmds.currentTime( query=True ) )
	def alt_i (self):
		x = self.getType(0)
		print x
	def ctrl_i (self):
		cmds.Import()
		#multipleFilters = "All Files (*.*);;Maya ASCii(*.ma);;Maya Binary(*.mb);;FBX (*.fbx);;Atom(*.atom)"
		#filename = cmds.fileDialog2(fileMode=1, caption="Import")
		#filename = cmds.fileDialog2 ( fileMode=1, fileFilter= multipleFilters, caption= "Import" )
		#cmds.file ( filename[0], i=True )
	###############################################      O      ###############################################
	def o (self):
		if self.getSelection() == 'None':
			cmds.playbackOptions( maxTime = cmds.currentTime( query=True ) )
		else:
			wireOn = cmds.modelEditor('modelPanel4', q=1, wos=1)
			if wireOn == True:
			    cmds.modelEditor('modelPanel4', edit = True, wos=0)
			else:
			    cmds.modelEditor('modelPanel4', edit = True, wos=1)
			cmds.select(deselect = 1)
	###############################################      C      ###############################################
	def c (self):
		if Cache.currentContext == 'myMove':
			cmds.snapMode( curve = True )
		else:
			if self.getSelection() == 'None':
				self.primitiveMenu()
			elif len(self.getSelection()) == 2:
				if self.getType(0)[0] == 'camera':
					self.constrainToParent('bake')
				else:
					self.constrainToParent('noBake', 'Maintain')
			else:
				print 'this is where we can place the convert or create tools'
	def c_release (self):
		cmds.snapMode( curve = False )
	def C (self):
		if self.getType(0) == 'locator' or self.getType(0)[0] == 'camera':
			cmds.color(ud = 2)
		elif self.getType(0) == 'face' or self.getType(0) == 'mesh':
			self.splitFaceTool()
		else:
			if Cache.currentCategory == 'frostbite':
				Cache.currentTool = ''
				self.cameraTool(Cache.currentCategory)
			else:
				Cache.currentTool = ''
				self.cameraTool() # just creates a normal camera, nothing special inside
		self.updateToolHUD()
	def C_release (self):
		cmds.snapMode( curve = False ) # it gets stuck for some reason and must be turned off
	def alt_c (self):
		self.sceneCamSwitch()
		# Activate lens HUD window
		x = cmds.window('FOV', query=1 , exists = 1)
		if x is False:
			self.lensHUD()
	def alt_shift_c (self):
		self.defaultCamSwitch()
	###############################################      H      ###############################################
	def h (self):
		self.hideGeometry()
	###############################################      V      ###############################################
	def v (self):
		cmds.snapMode( point = True )
	def v_release (self):
		cmds.snapMode( point = False )
	###############################################      X      ###############################################
	def x (self):
		cmds.snapMode( grid = True )
	def x_release (self):
		cmds.snapMode( grid = False )
	def alt_x (self):
		if Cache.currentCategory == 'modeling':
			if self.getType(0) == 'face':
				Cache.currentTool = 'Extrude Face'
				self.extrudeTool()
			elif self.getType(0) == 'edge':
				Cache.currentTool = 'Extrude Edge'
				self.extrudeTool()
			else:
				Cache.currentTool = ''
				cmds.warning('nothing selected')
		else:
			pass
		self.updateToolHUD()
	###############################################      S      ###############################################
	def S(self):
		if cmds.currentCtx() == 'polySlideEdgeContext':
			cmds.setToolTo ('polySelectEditContext')
		elif cmds.currentCtx() == 'polySelectEditContext':
			cmds.setToolTo ('polySlideEdgeContext')
		else:
			if self.getType(0) == 'edge':
				try:
					self.bridgeTool()
				except RuntimeError:
					cmds.setToolTo('polySlideEdgeContext')
			elif cmds.selectType(q=1, polymeshVertex = True) == True: #check to see if mask type is vertex
				self.vertexMergeTool()
			elif self.getType(0) == 'face':
				self.chipFacesTool()
			elif self.getType(0) == 'mesh':
				if len(self.getSelection()) == 1:
					self.polySeperateTool() # seperate because there's only one poly selected
				else:
					self.polyMergeTool() # merge because there's more than one poly selected
			elif self.getType(0)[0] == 'camera':
				print 'yes it is'
				self.cameraShakeTool()
			else:
				cmds.setToolTo ('polySelectEditContext')
	def alt_s (self):
		if self.getType(0) == 'mesh':
			self.getSharedGeo()
		elif self.getType(0) == 'face':
			self.getUVBoarder()
		else:
			currentCamera = cmds.modelEditor(Cache.modelPanel, query = 1, cam = 1)
			cmds.select(currentCamera)
	def alt_S (self):
		cmds.MergeToCenter()
	def ctrl_S(self):
		cmds.SaveSceneAs()
#HK = Hotkeys()