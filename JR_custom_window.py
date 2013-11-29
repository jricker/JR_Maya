import maya.cmds as cmds
def outlinerWindow():
	if cmds.window('outlinerWindow', exists = True):
		cmds.deleteUI('outlinerWindow', window = True)
	else:
		cmds.window('outlinerWindow')
		cmds.frameLayout( labelVisible=False )
		panel = cmds.outlinerPanel()
		outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
		cmds.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter' )
		cmds.showWindow()
def hyperWindow():
	if cmds.window('hyperGraphPanel1Window', query=True, exists= True):
		if cmds.window('hyperGraphPanel1Window', query = True, vis = True) == True:
			cmds.window('hyperGraphPanel1Window', edit = True, vis = False)
		else:
			cmds.window('hyperGraphPanel1Window', edit = True, vis = True)
	else:
		if cmds.scriptedPanel('hyperGraphPanel1', query = True, exists = True):
			cmds.scriptedPanel('hyperGraphPanel1', edit = True, tearOff = True)
			cmds.showWindow('hyperGraphPanel1Window')
		#cmds.window('hyperGraphPanel1Window', edit = True, vis = True)
def graphWindow():
	graphEditor = cmds.getPanel(scriptType = 'graphEditor')
	print graphEditor, ' this is graphEditor'
	for editors in graphEditor:
		graphEditorWindow = (editors + 'Window') 
		print graphEditorWindow, ' this is graphEditorWindow'
		if cmds.window(graphEditorWindow, exists = True):
			cmds.deleteUI(graphEditorWindow, window =True)
		else:
			cmds.scriptedPanel(editors, edit=True, to = True)