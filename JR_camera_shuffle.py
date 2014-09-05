from JR_cache_class import *
import maya.cmds as cmds
from JR_selection_class import Selection
Sel = Selection()
def createWindow(cameraList):
	#c = global.currentCamera()
	x = cmds.window('cameraWindow', query=1 , exists = 1)
	if x is False:
		print 'not found, creating window'
		cmds.window('cameraWindow', wh = [ 512, 288 ] )
		cmds.paneLayout()
		if Sel.getType(0)[1] == 'LIGHT' or Sel.getType(0)[1] == 'CAMERA':
			i = cmds.ls(selection=True)
		else:
			i = ('perspShape')
		Cache.modelPanel = cmds.modelPanel( mbv = 0, cam = i[0])
		cmds.modelEditor( Cache.modelPanel, edit=True, displayAppearance='smoothShaded', cameras = 1 )
		cmds.showWindow('cameraWindow')
	else:
		cmds.select( cameraList [Cache.camSceneOffset] )
		cmds.modelEditor(Cache.modelPanel, edit=True, cam = cameraList [Cache.camSceneOffset] )
def currentCamera():
	if Sel.getType(0)[1] == 'LIGHT' or Sel.getType(0)[1] == 'CAMERA':
		print 'going through current camera section in camera shuffle'
		i = cmds.ls(selection=True)
		cmds.modelEditor(Cache.modelPanel, edit=True, cam = i[0] )
	else:
		print 'select a camera or light'