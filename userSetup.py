import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utils
### CRITERION USER SETUPS ###
#cmds.evalDeferred("import pymel.core as pm")
#cmds.evalDeferred("import maya.mel as mel")
#cmds.evalDeferred("import sys")
#cmds.evalDeferred("sys.path.append('D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/')")
#cmds.evalDeferred("import pymel.core as pm")
#cmds.evalDeferred("import EAGR_toolsLauncher")
#cmds.evalDeferred("tool = EAGR_toolsLauncher.EAGR_toolsLauncher('D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/')")
#cmds.evalDeferred("gMainWindow = mel.eval('$temp1=$gMainWindow')")
#cmds.evalDeferred("oMenu= pm.menu(parent=gMainWindow, tearOff = True, label = 'EAGR ArtTools')")
#cmds.evalDeferred("pm.menuItem(parent=oMenu, label='EAGR_toolsLauncher', c='tool.m_main()')")
#mel.eval("putenv MAYA_SCRIPT_PATH (`getenv MAYA_SCRIPT_PATH` + \";\" + \"D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/MEL/\");")
#mel.eval("putenv MAYA_PLUG_IN_PATH (`getenv MAYA_PLUG_IN_PATH` + \";\" + \"D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/Plugins/\");")
#mel.eval("global string $EAGRToolsPath=\"D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/\"")
#mel.eval("source \"D:/nfs14/TnT/Tools/python/mayaPythonScripts/EAGR_toolsLauncher/EAGR_tools/mel/FrostbiteScripts.mel\" ")
### MY USER SETUPS ###
#cmds.headsUpDisplay( rp=(1, 0) ) # Need to remove the default occupied value before
#cmds.headsUpDisplay( rp=(1, 1) ) # Need to remove the default occupied value before
#cmds.headsUpDisplay( rp=(1, 2) ) # Need to remove the default occupied value before
#cmds.headsUpDisplay( rp=(1, 3) ) # Need to remove the default occupied value before
#cmds.headsUpDisplay( rp=(1, 4) ) # Need to remove the default occupied value before
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
utils.executeDeferred('setupHotkeys()')	# defer running command until everything is loaded and ready