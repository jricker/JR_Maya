import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utils
import os
### CRITERION USER SETUPS ###
if 'jricker' in os.path.expanduser("~"):
	cmds.evalDeferred("import pymel.core as pm")
	cmds.evalDeferred("import maya.mel as mel")
	cmds.evalDeferred("import sys")
	cmds.evalDeferred("sys.path.append('D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/')")
	cmds.evalDeferred("import pymel.core as pm")
	cmds.evalDeferred("import EAGR_toolsLauncher")
	cmds.evalDeferred("tool = EAGR_toolsLauncher.EAGR_toolsLauncher('D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/')")
	cmds.evalDeferred("gMainWindow = mel.eval('$temp1=$gMainWindow')")
	cmds.evalDeferred("oMenu= pm.menu(parent=gMainWindow, tearOff = True, label = 'EAGR ArtTools')")
	cmds.evalDeferred("pm.menuItem(parent=oMenu, label='EAGR_toolsLauncher', c='tool.m_main()')")
	mel.eval("putenv MAYA_SCRIPT_PATH (`getenv MAYA_SCRIPT_PATH` + \";\" + \"D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/MEL/\");")
	mel.eval("putenv MAYA_PLUG_IN_PATH (`getenv MAYA_PLUG_IN_PATH` + \";\" + \"D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/Plugins/\");")
	mel.eval("global string $EAGRToolsPath=\"D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/\"")
	#NEED TO BE FIXED!!!!! #mel.eval("source \"D:/projects/nfs15/PreProd/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/mel/FrostbiteScripts.mel\" ")
	## MY USER SETUPS ###
	#mel.eval("putenv MAYA_SCRIPT_PATH (`getenv MAYA_SCRIPT_PATH` + \";\" + \"C:/Users/jricker/Documents/GitHub/JR_Maya/\");")
	cmds.headsUpDisplay( rp=(1, 0) ) # Need to remove the default occupied value before
	cmds.headsUpDisplay( rp=(1, 1) ) # Need to remove the default occupied value before
	cmds.headsUpDisplay( rp=(1, 2) ) # Need to remove the default occupied value before
	cmds.headsUpDisplay( rp=(1, 3) ) # Need to remove the default occupied value before
	cmds.headsUpDisplay( rp=(1, 4) ) # Need to remove the default occupied value before
def sceneName():
	sceneNameFull = cmds.file(query = True, shortName = True, sceneName = True)
	return sceneNameFull
# Begin populating headsup boxes
cmds.ToggleCurrentFrame() # turns on the current frame hud
cmds.headsUpDisplay( 'categoryHUD', l = ':', ba = 'left' , s = 5, b=6)
cmds.headsUpDisplay( 'toolHUD', l = ':', ba = 'left', s = 5, b=7)
#
cmds.headsUpDisplay('cameraNameHUD', ba = 'left' , s = 5, b=5, pre='cameraNames')
cmds.headsUpDisplay('sceneNameHUD', ba = 'left' , s = 5, b=4 )
#
cmds.headsUpDisplay( 'nextAttrHUD',  l = '+',lfs = 'small',  s = 5, b=3)
cmds.headsUpDisplay( 'currAttrHUD',  l = '>>', lfs = 'small',dataFontSize = 'large', s = 5, b=2)
cmds.headsUpDisplay( 'prevAttrHUD', l = '-', lfs = 'small', s = 5, b=1)
#
def setupHotkeys():
	cmds.scriptEditorInfo(suppressWarnings=True) # supress annoying warnings
	from JR_hk_map	import *		# import user_hotkeys script
	Map.globalHotkeys() 				# init global hotkeys
	Map.setCategory('frostbite') 		# init category hotkeys
	# SET SCENE DEFAULTS
	cmds.setAttr ("defaultResolution.height", 720) # Frame Height
	cmds.setAttr ("defaultResolution.width", 1280) # Frame Width
	cmds.setAttr ("defaultResolution.deviceAspectRatio", 1.777) # Aspect Ratio
	cmds.setAttr ("defaultResolution.pixelAspect", 1) # Pixel Aspect
	cmds.currentUnit( time='ntsc') # Time - NTSC
	# SET CAMERA PLANES TO FAR AWAY::
	# FAR PLANE
	cmds.setAttr("perspShape.farClipPlane",  1000000 )
	cmds.setAttr("sideShape.farClipPlane",   1000000 )
	cmds.setAttr("topShape.farClipPlane",    1000000 )
	cmds.setAttr("frontShape.farClipPlane",  1000000 )
	# NEAR PLANE
	#cmds.setAttr("perspShape.nearClipPlane", 0.01 )
	#cmds.setAttr("sideShape.nearClipPlane",  0.01 )
	#cmds.setAttr("topShape.nearClipPlane",   0.01 )
	#cmds.setAttr("frontShape.nearClipPlane", 0.01 )
	# turn current frame off to start with
	mel.eval( "setCurrentFrameVisibility  (0) ;" )
	mel.eval( "setSceneTimecodeVisibility (0) ;" )
	mel.eval( "setFocalLengthVisibility   (0) ;" )
	# Set all of the defaults to what they should be.
	mel.eval( "setFrameRateVisibility (0) ; " )
	mel.eval( "setSelectDetailsVisibility (0) ; " )
	mel.eval( "setObjectDetailsVisibility (0) ; " )
	mel.eval( "setParticleCountVisibility (0) ; " )
	mel.eval( "setPolyCountVisibility (0) ; " )           #- maybe set this one to 1 if we go to modeling but 0 for the rest?
	mel.eval( "setSubdDetailsVisibility (0) ; " )         #- maybe set this one to 1 if we go to modeling but 0 for the rest?
	mel.eval( "setAnimationDetailsVisibility (0) ; " )    #- maybe set this to 1 for animation?
	mel.eval( "setHikDetailsVisibility (0) ; " )          #- maybe set this to 1 for animation?
	mel.eval( "setCurrentContainerVisibility (0) ; " )
	mel.eval( "setCameraNamesVisibility (0) ; " )
utils.executeDeferred('setupHotkeys()')	# defer running command until everything is loaded and ready