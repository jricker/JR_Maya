import maya.cmds as cmds
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
			cmds.button(label = 'modeling', c = self.setModeling )
			cmds.separator(w = categorySpace, style = 'none')
			cmds.button(label = 'frostbite', c = self.setFrostbite )
			cmds.separator(w = categorySpace, style = 'none')
			cmds.button(label = 'animation', c = self.setAnimation )
			cmds.showWindow('category')
	def lensChange(self, FOV ):
		currentCamera = cmds.ls(selection = True)
		#currentCamera = cmds.modelEditor(Cache.modelPanel, query = 1, cam = 1)
		cmds.camera(currentCamera , edit = True, focalLength = FOV)
	def lensHUD(self):
		# SHOW LENS BUTTONS
		cmds.window('FOV')
		cmds.rowColumnLayout(nc=1,cw=[(1,160)])
		cmds.button (l= '200', al='center', w= 160, h= 20, c= 'HUD.lensChange(200)' )
		cmds.button (l= '135', al='center', w= 160, h= 20, c= 'HUD.lensChange(135)' )
		cmds.button (l= '105', al='center', w= 160, h= 20, c= 'HUD.lensChange(105)' )
		cmds.button (l= '85',  al='center', w= 160, h= 20, c= 'HUD.lensChange(85) ' )
		cmds.button (l= '50',  al='center', w= 160, h= 20, c= 'HUD.lensChange(50) ' )
		cmds.button (l= '35',  al='center', w= 160, h= 20, c= 'HUD.lensChange(35) ' )
		cmds.button (l= '28',  al='center', w= 160, h= 20, c= 'HUD.lensChange(28) ' )
		cmds.button (l= '24',  al='center', w= 160, h= 20, c= 'HUD.lensChange(24) ' )
		cmds.button (l= '20',  al='center', w= 160, h= 20, c= 'HUD.lensChange(20) ' )
		cmds.showWindow('FOV')
	def playblastHUD(self):
		pass
	def removeWindow(self, category):
		cmds.deleteUI('category', window=True )
	def setModeling(self, *args):
		self.removeWindow('modeling')
		Map.setCategory('modeling')
	def setFrostbite(self, *args):
		self.removeWindow('frostbite')
		Map.setCategory('frostbite')
	def setAnimation(self, *args):
		self.removeWindow('animation')
		Map.setCategory('animation')
HUD = HUDs()