
###########################
###   MEASUREMENT TOOL  ###
###########################
import maya.cmds as cmds
sl = cmds.ls(selection=True, flatten = True)
oldLocators = cmds.ls(type = 'locator')
oldDistances = cmds.ls(type = 'distanceDimShape')
item1 = cmds.pointPosition( sl[0] )
item2 = cmds.pointPosition( sl[1] )
cmds.distanceDimension( startPoint = item1, endPoint= item2 )
newLocators = set(cmds.ls(type='locator')) - set(oldLocators)
newDistances = set(cmds.ls(type='distanceDimShape')) - set(oldDistances)
if len(newLocators) == 2:
    cmds.group(list(newLocators)[0], list(newLocators)[1] , list(newDistances)[0], n = 'measurement')
elif len(newLocators) == 1:
    cmds.group(list(newLocators)[0], list(newDistances)[0], n = 'measurement')
###########################
###    PLAYBLAST HUD3   ###
###########################
import maya.cmds as cmds
cmds.window(t='Playblast')
icon = cmds.internalVar(upd = True) + 'icons/JR_icons/folder.jpg'
mainLayout = cmds.columnLayout(w = 180, h = 80)
rowColumnLayout = cmds.rowColumnLayout(nc = 3, cw = [(1, 50), (2, 60), (3, 60)] , columnOffset = [(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)]   ) # first section relates to 1 and 2 columb widths
cmds.radioCollection()
cmds.text( label='Frame:', align = 'left' )
cmds.radioButton( label='1080' )
cmds.radioButton( label='720' )
cmds.radioCollection()
cmds.text( label='Format:', align = 'left' )
cmds.radioButton( label='avi' )
cmds.radioButton( label='mov' )
characerOptionMenu = cmds.optionMenu ( width = 160, label = 'Codec:    ')
cmds.text( label='')
cmds.text( label='' )
cmds.text( label='Custom:', align = 'left' )
customWidth = cmds.textField(text = 'W')
customHeight = cmds.textField(text = 'H')
inputField = cmds.textField( w =120, text = 'Location')
cmds.text( label='')
cmds.symbolButton(w=20, h=20, image = icon )
cmds.showWindow()
###########################
###    PLAYBLAST HUD2   ###
###########################
import maya.cmds as cmds
#    The following script will position the buttons in 2 rows, each
#    row a different height.
#
#    +----++----++----++----+
#    | b1 || b3 || b5 || b7 |
#    +----++----++----++----+
#    +----++----++----+
#    |    ||    ||    |
#    | b2 || b4 || b6 |
#    |    ||    ||    |
#    +----++----++----+
#
cmds.window()
cmds.rowColumnLayout( numberOfRows=1 )
cmds.button(l = 'Playblast')
#numberOfColumns=3, columnWidth=[(1, 60), (2, 80), (3, 100)] 
cmds.rowColumnLayout( numberOfColumns=4)
cmds.radioCollection()
cmds.separator(style = 'none'); cmds.separator(style = 'none'); cmds.separator(style = 'none'); cmds.separator(style = 'none')
cmds.separator( width=60, style='in' )
cmds.separator( width=60, style='in' )
cmds.separator( width=60, style='in' )
cmds.separator( width=60, style='in' )
cmds.text( label='  Size: ' )
#cmds.separator(style = 'none', w = 40)
cmds.radioButton( label='1080' )
cmds.radioButton( label='720' )
cmds.radioButton( label='640' )
cmds.text( label='Width:' )
customWidth = cmds.textField(w=5)
cmds.text( label='Height:' )
customHeight = cmds.textField(w=10)
cmds.separator(style = 'none')
cmds.separator(style = 'none')
cmds.separator(style = 'none')
#cmds.separator( width=60, style='in' )
cmds.showWindow()
###########################
###    PLAYBLAST HUD    ###
###########################
import maya.cmds as cmds
def change1():
    print 'one'
def change2():
    print 'two'
def change3():
    print 'three'
def lensHUD():
	cmds.window('FOV4')
	cmds.rowColumnLayout( nc=1,cw= [(2,60)] )
	cmds.radioCollection()
	cmds.separator(h= 10, style = 'none')
	cmds.text(label = "SIZE :", align = 'left')
	cmds.radioButton( label='  720' )
	cmds.radioButton( label='1080' )
	###
	cmds.separator(h= 10, style = 'none')
	cmds.text(label = "COMPRESSION :", align = 'left')
	cmds.radioCollection()
	cmds.radioButton( label='Sorenson 3' )
	cmds.radioButton( label='Quicktime' )
	cmds.radioButton( label='AVI' )
	cmds.separator(h= 10, style = 'none')
	cmds.button (l= 'PLAYBLAST', al='center', w= 160, h= 20, c= change1 )
	cmds.showWindow('FOV4')
lensHUD()

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
			sceneName = sceneNameFull
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


###########################
###  EULER ANGLES CODE  ###
###########################



#######################################################################################################################
## YOU CAN USE THIS METHOD FOR LINES AND VERTS ##
#######################################################################################################################
import maya.cmds as cmds
sl=cmds.ls(selection=True, flatten=True)
toVerts = cmds.polyListComponentConversion(sl, tv=True)
verts = cmds.ls(toVerts, flatten = True)
flatnormals = cmds.polyNormalPerVertex(verts, q=True, xyz=True)
normals = []
normals = zip(*[iter(flatnormals)]*3)
xNorm = [x[0] for x in normals]; xVector = sum(xNorm)/len(xNorm)
yNorm = [x[1] for x in normals]; yVector = sum(yNorm)/len(yNorm)
zNorm = [x[2] for x in normals]; zVector = sum(zNorm)/len(zNorm)
finalAngle = cmds.angleBetween( euler=True, v2= [xVector, yVector, zVector], v1=[0, 1, 0] )
## TEST OBJECT ALIGNMENT
cmds.xform('pCone1', ws = 1, ro = [ finalAngle[0], finalAngle[1] , finalAngle[2] ] )


#######################################################################################################################
### USE THIS METHOD FOR FACE SELECTION. STILL AN ISSUES IF OBJECT IS ROTATED, NEED TO CALCUATE THAT IN AS WELL SOMEHOW.
#######################################################################################################################
import maya.cmds as cmds
import decimal
## Poluate Vars
sl = cmds.ls(selection=True, flatten=True)
faceList = []
xValue  = []
yValue  = []
zValue  = []
# Find the face total and append it to the list
for i in sl:
	x = cmds.polyInfo( i, fn=True )
	faceList.append(x)
## Find the vectors for each face in the list
for i in faceList:
    vectors = str.split ( str(i[0])    )
    xValue.append ( float(vectors [2]) )
    yValue.append ( float(vectors [3]) )
    zValue.append ( float(vectors [4]) )
# Average the vectors from each x,y,z in face list
xAverage = ( sum(xValue) / len(xValue) )
yAverage = ( sum(yValue) / len(yValue) )
zAverage = ( sum(zValue) / len(zValue) )
# Find the angle in between Y up and the selected face vector
finalAngle = cmds.angleBetween(euler = True, v1 = [0, 1, 0] , v2 = [xAverage,yAverage,zAverage] )
# Test object for testing
cmds.xform('pCone1', ws = 1, ro = [ finalAngle[0], finalAngle[1] , finalAngle[2] ] )