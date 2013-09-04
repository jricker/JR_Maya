###########################
###    PLAYBLAST CODE   ###
###########################
import maya.cmds as cmds
import os
userPath = os.path.expanduser("~")
userFolder = os.path.dirname(userPath)
desktop = userFolder + '/Desktop/'
mayaCameraList = ['frontShape', 'perspShape', 'sideShape', 'topShape']
userCameraList = cmds.ls(cameras=True)
cameraSets =  set(userCameraList) - set(mayaCameraList)
allCameras = list(cameraSets)
currentSelection = cmds.ls(selection = True)
###
camerasSelected = []
for i in currentSelection:
	if cmds.objectType(i) == 'transform':
		#print 'it is a transform'
		getParent = cmds.listRelatives (i, s=True)
		checkType = cmds.objectType (getParent[0])
		if checkType == 'camera':
			camerasSelected.append(getParent[0])
def playblastStart(cameraList):
	for x in cameraList:
		i = cmds.listRelatives( x, p=True )
		cmds.select(i)
		start = cmds.findKeyframe( i, which="first" )
		end = cmds.findKeyframe( i, which="last" )
		sceneNameFull = cmds.file(query = True, shortName = True, sceneName = True)
		if '.mb' in sceneNameFull or '.ma' in sceneNameFull:
			sceneName = sceneNameFull[:-3] 
		else:
			sceneName = SceneNameFull
		cmds.select(cl = 1)
		focus = cmds.getPanel( withFocus=True )
		cmds.modelPanel( focus, edit=True, camera = x )
		cmds.modelEditor( focus, edit = True, cameras = False, locators = False)
		print start, end
		if start == end: # this means there's no keyframes
			print 'no keyframes on this one, playblasting timeline duration'
			cmds.playblast (format = "qt", compression = "Sorenson Video 3", filename = desktop + sceneName + '_' + str(i[0]) + '.mov', clearCache = 1 , viewer = 0, showOrnaments = 1, fp = 4, percent = 100, quality = 100, widthHeight = [1280, 720])
		else:
			print 'keyframes found, playblasting their start to end'
			cmds.playblast (startTime = start, endTime = end, format = "qt", compression = "Sorenson Video 3", filename = desktop + sceneName + '_' + str(i[0]) + '.mov', sequenceTime = 0, clearCache = 1 , viewer = 0, showOrnaments = 1, fp = 4, percent = 100, quality = 100, widthHeight = [1280, 720])
		#cmds.playblast( completeFilename = str(i) + '.mov', startTime = start, endTime = end, viewer = True, clearCache = True, percent = 100, quality = 100, format = "qt", framePadding = 20 )
		cmds.modelEditor( focus, edit = True, cameras = True, locators = True)
		print ' moving to the next one '
if len(camerasSelected) == 0:
	#print allCameras
	playblastStart(allCameras)
else:
	#print camerasSelected
	playblastStart(camerasSelected)