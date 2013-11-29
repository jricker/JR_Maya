import maya.cmds as cmds
import os
from functools import partial # this allows you to call a function with a button that has variables inside of it. Wihout it you can't do it. 
def UI():
	#establish the icon path
	icon = cmds.internalVar(upd = True) + 'icons/JR_icons/folder.jpg'
	#check for and create window
	if cmds.window('exampleBatchUI', exists = True):
		cmds.deleteUI('exampleBatchUI')
	window = cmds.window('exampleBatchUI', w = 500, h = 350, mnb = False, mxb = False, sizeable = False, title = 'Example Batch')
	# creat out main layout
	mainLayout = cmds.columnLayout(w = 500, h = 350)
	#create our row columb layout
	cmds.separator(h = 15)
	rowColumnLayout = cmds.rowColumnLayout(nc = 2, cw = [(1, 460), (2, 40)] , columnOffset = [(1, 'both', 5), (2, 'both', 5)]   ) # first section relates to 1 and 2 columb widths
	#input field
	cmds.text(label = 'Input Directory:', align='left')
	cmds.text(label = '') # this is to fill the next column with a blank for spacing
	inputField = cmds.textField('inputField', w = 460)
	cmds.symbolButton(w=20, h=20, image = icon, c = partial(browseFilePath, 3, None, 'inputField') )
	#seperator
	cmds.separator(h=5, style = 'none')
	cmds.separator(h=5, style = 'none')
	#text file field
	cmds.text(label = 'Text File:', align='left')
	cmds.text(label = '') # this is to fill the next column with a blank for spacing
	textInputField = cmds.textField('textInputField', w = 460)
	cmds.symbolButton(w=20, h=20, image = icon, c = partial(browseFilePath, 1, '*.txt', 'textInputField') )
	#seperator
	cmds.separator(h=5, style = 'none')
	cmds.separator(h=5, style = 'none')
	#output field
	cmds.text(label = 'Output Directory:', align='left')
	cmds.text(label = '') # this is to fill the next column with a blank for spacing
	outputField = cmds.textField('outputField', w = 460)
	cmds.symbolButton(w=20, h=20, image = icon, c = partial(browseFilePath, 3, None, 'outputField') )
	#seperator
	cmds.separator(h=5, style = 'none')
	cmds.separator(h=5, style = 'none')
	# process buddon
	cmds.button(w=500, h=50, label = 'Process', parent = mainLayout, c=process)
	# show window
	cmds.showWindow('exampleBatchUI')
def browseFilePath(fileMode, fileFilter, textField, *args):
	returnPath = cmds.fileDialog2(fileMode = fileMode, fileFilter = fileFilter, ds = 2 )[0]
	cmds.textField(textField, edit=True, text = returnPath)
def process(*args):
	inputDirectory = cmds.textField('inputField', q=True, text=True)
	textFile = cmds.textField('textInputField', q=True, text=True)
	outputDirectory = cmds.textField('outputField', q=True, text=True)
	files = os.listdir(inputDirectory)
	# filter the files
	for file in files:
		if file.rpartition('.')[2] == 'mb':
			fileName = inputDirectory +'/' + file
			#main loop
			cmds.file(fileName, open = True, force = True, ignoreVersion = True, prompt = False)
			print ' doing stuff'
			
	print inputDirectory, textFile, outputDirectory