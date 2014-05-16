import maya.cmds as cmds
import os
def UI():
	# check to see if the window exists
	if cmds.window('exampleUI', exists = True):
		cmds.deleteUI('exampleUI')
	#create the window
	window = cmds.window('exampleUI', title = 'exampleUI', w = 300, h = 300, mnb  = False, mxb = False, sizeable = False)
	#show window
	cmds.showWindow(window)
	# create a main layout
	mainLayout = cmds.columnLayout(h = 300, w = 300)
	# banner image
	imagePath = cmds.internalVar(userPrefDir = True) + 'icons' + '/test.jpg' # find the path to the image
	cmds.image(w = 300, h = 100, image = imagePath)
	cmds.separator(h = 15)# just a seperator
	# projects option menu
	projectsOptionMenu = cmds.optionMenu ( 'projectsOptionMenu', width = 300, changeCommand = populateCharacters, label = 'choose a project:     ') # change command needed to update character option menu based on what project is selected
	# create a character option menu
	characerOptionMenu = cmds.optionMenu ( 'characerOptionMenu', width = 300, label = 'choose a character: ')
	cmds.separator(h = 15) # just a seperator
	# create the build button
	cmds.button(label = 'build', w = 300, h = 50 ,c = build)
	# activate populate projects option menu
	populateProjects()
	# activate populate characaters option menu
	populateCharacters()
def populateProjects():
	projectPath = cmds.internalVar(userPrefDir = True).rpartition('prefs')[0] + 'projects/' # rpartition divides the string into 3 parts, 0, 1, and 2
	projects = os.listdir(projectPath)
	for project in projects:
		cmds.menuItem (label = project , parent = 'projectsOptionMenu')
def populateCharacters(*args): # just needs args put in because of the change command callback
	menuItems = cmds.optionMenu('characerOptionMenu', query = True, itemListLong = True)
	if menuItems != None: # this will clear out the character menu from pervious project selection but only if there is something there to begin with.
		for item in menuItems:
			cmds.deleteUI(item)
	selectedProject = cmds.optionMenu('projectsOptionMenu', q = True, v = True)
	projectPath = cmds.internalVar(userPrefDir = True).rpartition('prefs')[0] + 'projects/' + selectedProject + '/'# rpartition divides the string into 3 parts, 0, 1, and 2
	files = os.listdir(projectPath)
	characters = []
	for file in files:
		if file.rpartition('.')[2] == 'mb':
			characters.append(file)
	for character in characters:
		niceName = character.rpartition('.')[0]
		cmds.menuItem(label = niceName, parent = 'characerOptionMenu')
def build(*args):
	selectedProject = cmds.optionMenu('projectsOptionMenu', q = True, v = True)
	projectPath = cmds.internalVar(userPrefDir = True).rpartition('prefs')[0] + 'projects/' + selectedProject  + '/'
	selectedCharacter = cmds.optionMenu('characerOptionMenu', query = True, value = True)
	fileName = projectPath + selectedCharacter +'.mb'
	cmds.file(fileName, open = True, force = True, prompt = False)
UI()