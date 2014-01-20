import JR_custom_window
from JR_hud_class import *
from JR_tool_class import *
from JR_cache_class import *
from JR_attribute_class import *
from JR_selection_class import *
from JR_refresh_modules import *
class Hotkeys(Selection):
	def __init__(self):
		pass
	def tilde(self):
		Attribute.toggleUp()
	def alt_tilde(self):
		Attribute.toggleDown()
	def ctrl_tilde(self):
		HUD.displayMenu()
	###############################################      1      ###############################################
	def one(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			Tool.selectionMask( 'vertex' )
		else: # select mode is set to component
			if self.getType(0) == 'face' or self.getType(0) == 'edge': 
			# Check to see if another component is alread selected
			# This will switch the selection over
				cmds.select(Tool.convertSelection('vertex'))
				Tool.selectionMask( 'vertex' )
			else:
				if cmds.selectType( query = 1, polymeshVertex = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					Tool.selectionMask( 'vertex' )
	def alt_one(self):
		JR_custom_window.outlinerWindow()
	###############################################      2      ###############################################
	def two(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			Tool.selectionMask( 'edge' )
		else: # select mode is set to component
			if self.getType(0) == 'face':
				cmds.select(Tool.convertSelection('edge'))
				Tool.selectionMask( 'edge' )
			elif self.getType(0) == 'vertex':
				cmds.select(Tool.convertSelection('edgeBorder'))
				Tool.selectionMask( 'edge' )
			else:
				if cmds.selectType( query = 1, polymeshEdge = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					Tool.selectionMask( 'edge' )
	def alt_two(self):
		JR_custom_window.hyperWindow()
	###############################################      3      ###############################################
	def three(self):
		if cmds.selectMode ( query = 1, object = 1):
			cmds.selectMode ( component = 1)
			Tool.selectionMask( 'face' )
		else: # select mode is set to component
			if self.getType(0) == 'vertex' or self.getType(0) == 'edge':
				cmds.select(Tool.convertSelection('face'))
				Tool.selectionMask( 'face' )
			else:
				if cmds.selectType( query = 1, polymeshFace = True):
					cmds.selectMode ( object = 1)
					cmds.selectType( allComponents = False )
				else:
					Tool.selectionMask( 'face' )
	def alt_three(self):
		JR_custom_window.graphWindow()
	###############################################      4      ###############################################
	def alt_four(self):
		cmds.HypershadeWindow()
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
		Tool.selectTool()
	def q_release(self):
		print 'claiming "q" release from default maya'
		HUD.updateToolHUD()
	def alt_q(self):
		Cache.keyOffset = 2
		Cache.currentTool = 'select - attrs'
		Tool.selectTool()
		HUD.updateToolHUD()
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
		Tool.moveTool()
	def w_release(self):
		print 'claiming "w" release from default maya'
		HUD.updateToolHUD()
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
		Tool.rotateTool()
	def e_release(self):
		print 'claiming "e" release from default maya'
		HUD.updateToolHUD()
	def alt_e(self):
		if Cache.currentCategory == 'frostbite':
			Cache.currentTool = 'Importing Assets'
			Tool.exportTool(Cache.currentCategory)
		else:
			Cache.currentTool = ''
			cmds.warning(' only works with Frostbite category right now')
		HUD.updateToolHUD()
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
		Tool.scaleTool()
	def R (self):
		RELOAD.refreshAll()
		cmds.warning('All Modules Refreshed :)')
	def r_release(self):
		print 'claiming "r" release from default maya'
		HUD.updateToolHUD()
	def alt_r(self):
		Tool.renameTool()
		HUD.updateToolHUD()
	def ctrl_r(self):
		cmds.ReferenceEditor()
	###############################################      L      ###############################################
	def ctrl_l (self):
		Tool.createInMiddle("cmds.spaceLocator( name = 'JR_locator_01', position = (0,0,0) )")
		if Cache.locatorList != []:
			newLocators = self.getSelection()
			#print Cache.locatorList, ' this is the cache list'
			#print self.getSelection(), 'this is the locator list'
			# automatically bake the locators if more than one has been created, because I would only create more than one if it was necessary for verts of faces.
			parentObject = self.getParent(Cache.locatorList[0] )
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
		HUD.playblastHUD()
	def ctrl_p(self):
		if self.getType(0) == 'face' or self.getType(0) == 'mesh':
			print ' not sure which tool should go here .. '
	###############################################      F      ###############################################
	#def f (self):
	#	cmds.viewFit(animate = False)
	#def f_release(self):
	#	pass
	def F (self):
		# Sets a Keyframe on the focal length of a camera if selected - Just like Shift + w sets a keyframe on the move attr
		if self.getType(0)[1] == 'CAMERA':
			currentCamera = self.getSelection()
			cmds.setKeyframe(str(currentCamera[0]) + '.fl')
		if self.getType(0) == 'edge':
			cmds.polyCloseBorder()
	###############################################      M      ###############################################
	def ctrl_m (self):
		HUD.mirrorMenu( Tool.mirrorModelingTool )
	###############################################      B      ###############################################
	def alt_b (self):
		if self.getSelection() == 'None':
			cmds.CycleBackgroundColor() # cycles the background color as per the default
		else:
			if self.getType(0) == 'face' or self.getType(0) == 'vertex' or self.getType(0) == 'edge':
				Tool.bevelTool()
			# switch this over to recognize the animation category later on istead of just fitting to a camera selection. Should be able to work on any object selected
			else:
				start = cmds.findKeyframe( self.getSelection(), which = "first" )
				end = cmds.findKeyframe( self.getSelection(), which = "last" )
				if start == end: # this means there's no keyframes
					start = cmds.playbackOptions(q=1, minTime=1)
					end =   cmds.playbackOptions(q=1, maxTime=1)
				cmds.bakeSimulation(self.getSelection(), time =(start,end), sampleBy = 1 )

	###############################################      D      ###############################################
	def d (self):
		# Tool To create the measurement tool when vertexes are selected
		if self.getType(0) == 'vertex':
			sl = cmds.ls(selection=True, flatten = True)
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
			Tool.smoothTool()
		HUD.updateToolHUD()
	###############################################      A      ###############################################
	#def a (self):
	#	cmds.viewFit(all = True, animate = False)
	#def a_release(self):
	#	pass
	###############################################      I      ###############################################
	def i (self):
		cmds.playbackOptions( minTime = cmds.currentTime( query=True ) )
	def alt_i (self):
		x = self.getType(0)
		print x
	def ctrl_i (self):
		multipleFilters = "All Files (*.*);;Maya ASCii(*.ma);;Maya Binary(*.mb);;FBX (*.fbx);;Atom(*.atom)"
		#filename = cmds.fileDialog2(fileMode=1, caption="Import")
		filename = cmds.fileDialog2 ( fileMode=1, fileFilter= multipleFilters, caption= "Import" )
		cmds.file ( filename[0], i=True )
	###############################################      O      ###############################################
	def o (self):
		cmds.playbackOptions( maxTime = cmds.currentTime( query=True ) )
	###############################################      C      ###############################################
	def c (self):
		if Cache.currentContext == 'myMove':
			cmds.snapMode( curve = True )
		else:
			if self.getType(0) == 'None':
				HUD.primitiveMenu()
			else:
				print 'this is where we can place the convert or create tools'
	def c_release (self):
		cmds.snapMode( curve = False )
	def C (self):
		if self.getType(0) == 'locator' or self.getType(0)[0] == 'camera':
			cmds.color(ud = 2)
		elif self.getType(0) == 'face' or self.getType(0) == 'mesh':
			Tool.splitFaceTool()
		else:
			if Cache.currentCategory == 'frostbite':
				Cache.currentTool = ''
				Tool.cameraTool(Cache.currentCategory)
			else:
				Cache.currentTool = ''
				Tool.cameraTool() # just creates a normal camera, nothing special inside
		HUD.updateToolHUD()
	def C_release (self):
		cmds.snapMode( curve = False ) # it gets stuck for some reason and must be turned off
	def alt_c (self):
		Tool.sceneCamSwitch()
		# Activate lens HUD window
		x = cmds.window('FOV', query=1 , exists = 1)
		if x is False:
			HUD.lensHUD()
	def alt_shift_c (self):
		Tool.defaultCamSwitch()
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
				Tool.extrudeTool()
			elif self.getType(0) == 'edge':
				Cache.currentTool = 'Extrude Edge'
				Tool.extrudeTool()
			else:
				Cache.currentTool = ''
				cmds.warning('nothing selected')
		else:
			pass
		HUD.updateToolHUD()
	###############################################      S      ###############################################
	def S(self):
		if cmds.currentCtx() == 'polySlideEdgeContext':
			cmds.setToolTo ('polySelectEditContext')
		elif cmds.currentCtx() == 'polySelectEditContext':
			cmds.setToolTo ('polySlideEdgeContext')
		else:
			if self.getType(0) == 'edge':
				Tool.bridgeTool()
			elif cmds.selectType(q=1, polymeshVertex = True) == True: #check to see if mask type is vertex
				Tool.vertexMergeTool()
			elif self.getType(0) == 'face':
				Tool.chipFacesTool()
			elif self.getType(0) == 'mesh':
				if len(self.getSelection()) == 1:
					Tool.polySeperateTool() # seperate because there's only one poly selected
				else:
					Tool.polyMergeTool() # merge because there's more than one poly selected
			elif self.getType(0)[0] == 'camera':
				print 'yes it is'
				Tool.cameraShakeTool()
			else:
				cmds.setToolTo ('polySelectEditContext')
	def alt_s (self):
		currentCamera = cmds.modelEditor(Cache.modelPanel, query = 1, cam = 1)
		cmds.select(currentCamera)
	def ctrl_S(self):
		cmds.SaveSceneAs()
HK = Hotkeys()