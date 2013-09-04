import JR_custom_window
from JR_hud_class import *
from JR_tool_class import *
from JR_cache_class import *
from JR_attribute_class import *
from JR_selection_class import *
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
	###############################################      Q      ###############################################
	def q (self):
		offsetCount = 2
		if self.getContext() == 'mySelect' or self.getContext() == 'myPaintSelect':
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
			print ' only works with Frostbite category right now'
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
	def r_release(self):
		print 'claiming "r" release from default maya'
		HUD.updateToolHUD()
	def alt_r(self):
		Tool.renameTool()
		HUD.updateToolHUD()
	###############################################      L      ###############################################
	def ctrl_l (self):
		cmds.spaceLocator( name = 'JR_locator_01', position = self.getMiddle())
		cmds.xform(centerPivots=True)
	###############################################      P      ###############################################
	def alt_p (self):
		Tool.playblastTool()
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
	###############################################      A      ###############################################
	#def a (self):
	#	cmds.viewFit(all = True, animate = False)
	#def a_release(self):
	#	pass
	###############################################      I      ###############################################
	def ctrl_i (self):
		multipleFilters = "All Files (*.*);;Maya ASCii(*.ma);;Maya Binary(*.mb);;FBX (*.fbx);;Atom(*.atom)"
		#filename = cmds.fileDialog2(fileMode=1, caption="Import")
		filename = cmds.fileDialog2 ( fileMode=1, fileFilter= multipleFilters, caption= "Import" )
		cmds.file ( filename[0], i=True )
	###############################################      C      ###############################################
	def c (self):
		cmds.snapMode( curve = True )
	def c_release (self):
		cmds.snapMode( curve = False )
	def C (self):
		if Cache.currentCategory == 'frostbite':
			Cache.currentTool = ''
			Tool.cameraTool(Cache.currentCategory)
		else:
			Cache.currentTool = ''
			print ' only works with Frostbite category right now'
		HUD.updateToolHUD()
	def C_release (self):
		cmds.snapMode( curve = False ) # it gets stuck for some reason and must be turned off
	def alt_c (self):
		Tool.sceneCamSwitch()
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
			else:
				Cache.currentTool = ''
				print 'nothing selected'
		HUD.updateToolHUD()
	###############################################      S      ###############################################
	def alt_s (self):
		currentCamera = cmds.modelEditor(Cache.modelPanel, query = 1, cam = 1)
		cmds.select(currentCamera)
HK = Hotkeys()