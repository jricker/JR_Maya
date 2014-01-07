import maya.cmds as cmds
from functools import partial
from JR_tool_class import *
from JR_hk_map import *
from JR_selection_class import *
class HUDs(Selection):
	def __init__(self):
		pass
	def updateToolHUD(self):
		cmds.headsUpDisplay( 'toolHUD', edit = True, c = self.setToolHUD )
	def setToolHUD(self):
		return Cache.currentTool
	def displayMenu(self):
		categorySpace = 5
		if cmds.window('category', exists=True):
			cmds.deleteUI('category', window=True )
		else:
			cmds.window( 'category', h=20, titleBar = 0, s=0)
			cmds.rowColumnLayout( numberOfRows=1, rs = [10, 10])
			cmds.button(label = 'CUBE',  c = partial(self.setCategory, 'modeling' ) ) # MODELING
			cmds.separator(w = categorySpace, style = 'none')
			cmds.button(label = 'SPHERE', c = partial(self.setCategory, 'frostbite') ) # FROSTBITE
			cmds.separator(w = categorySpace, style = 'none')
			cmds.button(label = 'animation', c = partial(self.setCategory, 'animation') ) # ANIMATION
			cmds.separator(w = categorySpace, style = 'none')
			cmds.button(label = 'uv', c = partial(self.setCategory, 'uv') ) # UV
			cmds.showWindow('category')
	def primitiveMenu(self):
		categorySpace = 5
		if cmds.window('primitives', exists=True):
			cmds.deleteUI('primitives', window=True )
		else:
			window = cmds.window(sizeable = 0 )
			cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 40), (2, 40), (3, 40)] )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCube()', image1='polyCube.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polySphere()', image1='polySphere.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='polyCylinder.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='polyTorus.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='polyCone.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='polyPyramid.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='polyPipe.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.setToolTo("CreatePolyPlaneCtx")', image1='polyMesh.png' )
			cmds.nodeIconButton( style='iconOnly', command='cmds.polyCylinder()', image1='curveEP.png' )
			cmds.showWindow( window )
			#cmds.window( 'primitives', h=20, titleBar = 0, s=0)
			#cmds.rowColumnLayout( numberOfRows=1, rs = [10, 10])
			#cmds.button(label = 'modeling',  c = partial(self.setCategory, 'modeling' ) ) # MODELING
			#cmds.separator(w = categorySpace, style = 'none')
			#cmds.button(label = 'frostbite', c = partial(self.setCategory, 'frostbite') ) # FROSTBITE
			#cmds.separator(w = categorySpace, style = 'none')
			#cmds.button(label = 'animation', c = partial(self.setCategory, 'animation') ) # ANIMATION
			#cmds.separator(w = categorySpace, style = 'none')
			#cmds.button(label = 'uv', c = partial(self.setCategory, 'uv') ) # UV
			#cmds.showWindow('primitives')
	def lensChange(self, FOV, *args ):
		currentCamera = cmds.ls(selection = True)
		#currentCamera = cmds.modelEditor(Cache.modelPanel, query = 1, cam = 1)
		cmds.camera(currentCamera , edit = True, focalLength = FOV)
	def lensHUD(self):
		# SHOW LENS BUTTONS
		cmds.window('FOV')
		cmds.rowColumnLayout(nc=1,cw=[(1,160)])
		cmds.button (l= '200', al='center', w= 160, h= 20, c= partial( self.lensChange, 200 ) )
		cmds.button (l= '135', al='center', w= 160, h= 20, c= partial( self.lensChange, 135 ) )
		cmds.button (l= '105', al='center', w= 160, h= 20, c= partial( self.lensChange, 105 ) )
		cmds.button (l= '85',  al='center', w= 160, h= 20, c= partial( self.lensChange,  85 ) )
		cmds.button (l= '50',  al='center', w= 160, h= 20, c= partial( self.lensChange,  50 ) )
		cmds.button (l= '35',  al='center', w= 160, h= 20, c= partial( self.lensChange,  35 ) )
		cmds.button (l= '28',  al='center', w= 160, h= 20, c= partial( self.lensChange,  28 ) )
		cmds.button (l= '24',  al='center', w= 160, h= 20, c= partial( self.lensChange,  24 ) )
		cmds.button (l= '20',  al='center', w= 160, h= 20, c= partial( self.lensChange,  20 ) )
		cmds.showWindow('FOV')
	###############################################  PLAYBLAST  ###############################################
	def playblastHUD(self):
		if cmds.window('pb', exists = True):
			cmds.deleteUI('pb')
		window = cmds.window('pb', titleBar = 0, sizeable = False)
		icon = cmds.internalVar(upd = True) + 'icons/JR_icons/folder.jpg' # FOLDER ICON
		mainLayout = cmds.columnLayout(w = 180, h = 80)
		# Row and Column Layout Setup
		cmds.rowColumnLayout(nc = 3, cw = [(1, 50), (2, 60), (3, 60)] , columnOffset = [(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)]   ) # first section relates to 1 and 2 columb widths
		# Radio Button Collection For 1080 and 720
		cmds.radioCollection()
		frameSize = cmds.text( label='Frame:', align = 'left' )
		i1080 = cmds.radioButton( label='1080', onc = partial( self.playblastSize, '1080' ) )
		i720 = cmds.radioButton( label='720',  onc = partial( self.playblastSize, '720'  ) )
		if Cache.playblastSize == [1920, 1080]:
			cmds.radioButton ( i1080, edit = True, select = True )
		elif Cache.playblastSize == [1280, 720]:
			cmds.radioButton ( i720, edit = True, select = True )
		# Radio Button Collection For AVI and MOV
		formatType = cmds.radioCollection()
		cmds.text( label='Format:', align = 'left' )
		avi = cmds.radioButton( label='avi', onc = partial( self.playblastFormat, 'avi' ) )
		qt = cmds.radioButton( label='mov', onc = partial( self.playblastFormat, 'qt' ) )
		if Cache.playblastFormat == 'qt':
			cmds.radioButton ( qt, edit = True, select = True )
		elif Cache.playblastFormat == 'avi':
			cmds.radioButton ( avi, edit = True, select = True )
		# Codec Section
		codecOptionMenu = cmds.optionMenu ('codecOptionMenu', width = 160, label = 'Codec:    ' ); cmds.text( label=''); cmds.text( label='' )
		self.playblastFormat(Cache.playblastFormat)
		menuItems = cmds.optionMenu('codecOptionMenu', query = True, itemListLong = True)
		if Cache.playblastCodec in menuItems:
			cmds.optionMenu ('codecOptionMenu', e=True, v=Cache.playblastCodec)
		# Custom Width and Height Area
		#cmds.text( label='Custom:', align = 'left' ); customWidth = cmds.textField(text = 'W'); customHeight = cmds.textField(text = 'H')
		# Location of Playblasts
		inputField = cmds.textField( w =120, text = 'Change Location')
		cmds.text( label='')
		cmds.symbolButton(w=20, h=20, image = icon )
		# focus on input field so when enter is pressed it can just begin
		cmds.setFocus(inputField) 
		# Button to start the playblast
		cmds.button(w=180, h=30, label = 'PLAYBLAST', parent = mainLayout, c= partial( self.playblastExecute ) )
		#cmds.textField(inputField, edit = True, alwaysInvokeEnterCommandOnReturn = True, enterCommand = partial( self.playblastExecute ) )
		cmds.showWindow(window)
	def playblastFormat(self, format, *args):
		if format == 'avi':
			Cache.playblastFormat = 'avi'
			codecs = ['none', "MS-YUV", "IYUV codec"]
		elif format == 'qt':
			Cache.playblastFormat = 'qt'
			codecs = ['Sorenson Video 3', 'h264']
		#
		menuItems = cmds.optionMenu('codecOptionMenu', query = True, itemListLong = True)
		if menuItems != None: # this will clear out the character menu from pervious project selection but only if there is something there to begin with.
			for item in menuItems:
				cmds.deleteUI(item)
		for i in codecs:
			cmds.menuItem (label = i , parent = 'codecOptionMenu')
	def playblastSize(self, size, *args):
		if size == '1080':
			Cache.playblastSize = [1920, 1080]
		elif size == '720':
			Cache.playblastSize = [1280, 720]
	def playblastExecute(self, *args):
		selectedCodec = cmds.optionMenu('codecOptionMenu', q = True, v = True)
		Cache.playblastCodec = selectedCodec
		cmds.deleteUI('pb')
		Tool.playblastTool( [Cache.playblastFormat, Cache.playblastCodec, Cache.playblastSize] )
	###############################################             ###############################################
	###############################################             ###############################################
	def setCategory(self, category, *args):
		cmds.deleteUI('category', window=True )
		Map.setCategory(category)
HUD = HUDs()