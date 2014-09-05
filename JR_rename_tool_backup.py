import maya.cmds as cmds
from functools import partial
from JR_rename_class import Rename
class RenameTool(Rename):
	def __init__(self):
		Rename.__init__(self)
def UI(processCall = 'NA'):
	refItem = cmds.ls(selection = True, flatten=True); sortedRef = sorted(refItem) #orderedSelection=True - this was in the ls, took it out
	if sortedRef == []:sortedRef.append('nothing selected') #Used if nothing is selected in scene but tool is called.
	if cmds.window('renameUI', exists = True):
		cmds.deleteUI('renameUI')
	window = cmds.window("renameUI", w = 200, h = 100, mnb = False, mxb = False, title = "Rename Selection", sizeable = False)
	mainLayout = cmds.columnLayout(w = 200, h=100)
	cmds.text(label = "Name", align = 'left')
	cmds.textField("inputField", w=200, text=sortedRef[0])
	cmds.textField("replaceField", w=200)
	cmds.text(label = "Replace Top with Bottom", align = 'right')
	cmds.textField("withField", w=200)
	# add functions
	cmds.textField('inputField', edit = True, alwaysInvokeEnterCommandOnReturn = True, enterCommand = partial (process, processCall) )
	cmds.textField("replaceField", edit = True, alwaysInvokeEnterCommandOnReturn = True, enterCommand = partial (process, processCall) )
	cmds.textField("withField", edit = True, alwaysInvokeEnterCommandOnReturn = True, enterCommand = partial (process, processCall) )
	cmds.setFocus('withField') # set focus to the with field so it's easier to just tab to the input field
	cmds.showWindow(window)
####
def process( call, *args):
	# Selection
	intialSelection = cmds.ls(selection=True, flatten=True)
	selections = intialSelection[:]
	# Input Values from UI
	inputName = ['placeholder'] # needs to be a list fed into it to work
	inputName[0] = cmds.textField("inputField", q=True, text = True)
	old = cmds.textField("replaceField", q=True, text = True)
	new = cmds.textField("withField", q=True, text = True)
	# Assign the Rename Class 
	D = Rename(selections, inputName )
	if old: # if there is data in the replaceField txt box, then run the replacement code
		for i in range( len (selections) ):
			findTxt = D.reFunction(D.getAfterNamespace(i), old)
			replacementName = D.getAfterNamespace(i)[ : findTxt [0][0] ] + new + D.getAfterNamespace(i)[ findTxt [0][1] : ]
			cmds.rename(selections[i], D.getNamespace(i) + replacementName)
	else:
		for i in range( len (selections) ):
			X = D.processNamespace(i)
			if X == ':': X = '::' # This prevents the root namespace from getting lost in the cutoff [:-1] use X[:-1] instead of D.processNamespace(i) [:-1]
			if cmds.namespace(exists = X [:-1] ) != True: # creates new namespace if doesn't already exist
				print ' creating new namespace'
				cmds.namespace(addNamespace = X [:-1] ) # create namespace if doesn't already exist
			cmds.rename( D.selection[i] , ':' + D.processNamespace(i) + D.processRename(i) )
			cmds.namespace(set = ':') # set namespace back to root so any new object created is under the root
	if call == 'NA':
		cmds.warning('no exit call, window stays open')
	elif call == 'exit':
		cmds.warning('exit called, closing rename window')
		cmds.evalDeferred('cmds.deleteUI("renameUI")')
		#cmds.deleteUI(window)