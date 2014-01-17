import maya.cmds as cmds
import maya.mel as mel
def setSceneHUD():
	return cmds.file(query = True, shortName = True, sceneName = True)
def resetSceneHUD():
	return ''
def playblastStart(cameraList, directory, formatInfo):
	focus = cmds.getPanel( withFocus=True )
	## set attributes for Viewport 2.0
	cmds.modelEditor( focus, edit = True, cameras = False, locators = False, grid = 0, lights = 0, displayTextures =1, textureHilight = 1, shadows = 1,  rendererName = 'ogsRenderer' ) # sets viewport to Viewport 2.0
	if len(cmds.ls(lights = 1) ) == 0:
		cmds.modelEditor( focus, edit = 1, displayLights = 'default' )
	else:
		cmds.modelEditor( focus, edit = 1, displayLights = 'all' )
	# motion blur on
	cmds.setAttr ("hardwareRenderingGlobals.motionBlurEnable", 1)
	cmds.setAttr ("hardwareRenderingGlobals.motionBlurShutterOpenFraction", 0.1 )
	cmds.setAttr ("hardwareRenderingGlobals.motionBlurSampleCount", 32)
	# anti aliasing on
	cmds.setAttr ("hardwareRenderingGlobals.multiSampleEnable", 1)
	cmds.setAttr ("hardwareRenderingGlobals.multiSampleCount", 16)
	# screen space AO
	cmds.setAttr ("hardwareRenderingGlobals.ssaoEnable", 1)
	cmds.setAttr ("hardwareRenderingGlobals.ssaoAmount", .5)
	cmds.setAttr ("hardwareRenderingGlobals.ssaoRadius", 25)
	cmds.setAttr ("hardwareRenderingGlobals.ssaoFilterRadius", 25)
	cmds.setAttr ("hardwareRenderingGlobals.ssaoSamples", 32)
	if formatInfo[0] == 'qt':
		fileExtension = '.mov'
	elif formatInfo[0] == 'avi':
		fileExtension = '.avi'
	# setup the HUD elements to be visible
	mel.eval( "setCurrentFrameVisibility  (1) ;" )
	mel.eval( "setSceneTimecodeVisibility (1) ;" )
	mel.eval( "setFocalLengthVisibility   (1) ;" )
	cmds.headsUpDisplay( 'sceneNameHUD', edit = True, c = setSceneHUD )
	#
	for x in cameraList:
		# cache current clipping planes just in case we need them for some reason
		near = cmds.getAttr(str(x) + '.nearClipPlane')
		far = cmds.getAttr(str(x) +'.farClipPlane')
		# Set attrs to avoid clipping issues
		cmds.setAttr(str(x) + '.nearClipPlane', 0.1 )
		cmds.setAttr(str(x) + '.farClipPlane', 100000 )
		cmds.setAttr( str(x) + '.bestFitClippingPlanes', False )
		#
		cmds.select(x)
		start = cmds.findKeyframe( x, which="first" )
		end = cmds.findKeyframe( x, which="last" )
		sceneNameFull = cmds.file(query = True, shortName = True, sceneName = True)
		if '.mb' in sceneNameFull or '.ma' in sceneNameFull:
			sceneName = sceneNameFull[:-3]
		else:
			sceneName = SceneNameFull
		cmds.modelPanel ( focus, edit=True, camera = x )
		if start == end: # this means there's no keyframes
			cmds.warning ('no keyframes found on ' + str(x) + ', playblasting timeline duration' )
			cmds.playblast (format = formatInfo[0], compression = formatInfo[1], forceOverwrite = 1, showOrnaments = 1, filename = directory + sceneName + '_' + x + fileExtension , clearCache = 1 , viewer = 0, percent = 100, quality = 100, widthHeight = formatInfo[2] )
		else:
			cmds.warning('keyframes found on ' + str(x) + ', playblasting ' + str(start) + ' to ' + str(end) )
			cmds.playblast (startTime = start, endTime = end, format = formatInfo[0], compression = formatInfo[1], forceOverwrite = 1, showOrnaments = 1, filename = directory + sceneName + '_' + x + fileExtension , clearCache = 1 , viewer = 0, percent = 100, quality = 100, widthHeight = formatInfo[2] )
		# Set attrs back to normal 
		cmds.setAttr(str(x) + '.nearClipPlane', near )
		cmds.setAttr(str(x) + '.farClipPlane', far )
		cmds.setAttr( str(x) + '.bestFitClippingPlanes', True )
	####
	mel.eval( "setCurrentFrameVisibility  (0) ;" )
	mel.eval( "setSceneTimecodeVisibility (0) ;" )
	mel.eval( "setFocalLengthVisibility   (0) ;" )
	####
	cmds.headsUpDisplay( 'sceneNameHUD', edit = True, c = resetSceneHUD )
	cmds.modelEditor( focus, edit = True, cameras = True, locators = True, grid = 1, lights = 1, displayTextures=0, shadows = 0, displayLights = 'default' , rendererName = 'base_OpenGL_Renderer', camera = 'persp'  ) # sets viewport back to default