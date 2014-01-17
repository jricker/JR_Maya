import maya.cmds as cmds
from JR_hud_class import *
from JR_cache_class import *
from JR_selection_class import *
from JR_attribute_class import *
################################### CAN USE THE PYTHON HOTKEY COMMAND TO IDENTIFY CUSTOM MODIFIERS WHEN DRAG TOOL IS BEING RUN ##################
class DraggerTool(Selection):
	def __init__(self):
		self.dragDirection = []
	def __call__(self, selection = 'NA' , historyName = '' ):
		if selection == 'NA':
			selection = self.getSelection()
		#self.selection = selection
		#print self.selection, ' this is the selection'
		self.history = self.getHistory(selection, -1, historyName)
		self.attribute = self.history[-1] + Cache.currentAttribute
		print self.attribute, ' this is the start attribute'
		#self.attributeValue = cmds.getAttr( self.attribute )
		try:
			cmds.draggerContext( 'dragTool', edit=True, pressCommand= ('Dragger.pressFunction()'), dragCommand= ('Dragger.dragFunction()'), finalize = ('Dragger.exitFunction()'),  undoMode = "step")
		except:
			cmds.draggerContext( 'dragTool', pressCommand= ('Dragger.pressFunction()'), dragCommand= ('Dragger.dragFunction()'), finalize = ('Dragger.exitFunction()'), undoMode = "step" )
		cmds.setToolTo( 'dragTool' )
	def exitFunction(self):
		# Reset Attribute Hud and Tool Hud
		#Attribute.setAttributes()
		#Cache.currentTool = ''
		#HUD.updateToolHUD()
		print 'exiting dragger tool'
	def pressFunction(self):
		self.attribute = self.history[-1] + Cache.currentAttribute # re-init the attribute in case cached has been switched
		self.modifier = cmds.draggerContext( 'dragTool', query=True, modifier=True)
		self.button = cmds.draggerContext('dragTool', query = True, button=True)
		self.attributeValue = cmds.getAttr( self.attribute )
		if cmds.currentUnit( query=True, linear=True ) == 'cm':
			self.speed = .01 # modifier for speed traveled through values while dragging
		elif cmds.currentUnit( query=True, linear=True ) == 'm':
			self.speed = .001 # modifier for speed traveled through values while dragging
		else:
			self.speed = .0001
		self.space = 'screen' # initialize the variable
		if isinstance(self.attributeValue, list): # only edit the space based on button if the attribute is a list value
			# If left click is used, then the space is set to (X,Y,Z) world based
			# If middle click is used, space is set to (X, Y) screen based
			if self.button == 1: # left button
				self.space = 'world' # tracking space used
				cmds.draggerContext( 'dragTool', edit=True, space = 'world')
			elif self.button == 2: # middle button
				self.space = 'screen' # tracking space used
				cmds.draggerContext( 'dragTool', edit=True, space = 'screen')
		else: # set to 'screen' as default if the attr isn't a list value
			cmds.draggerContext( 'dragTool', edit=True, space = 'screen')
		if self.modifier == 'ctrl':
			self.speed = self.speed * .01
			#self.speedY = self.speedY * .01
		if self.modifier == 'shift':
			self.speed = self.speed * 10
			#self.speedY = self.speedY * 10
		if len(self.dragDirection) > 0:
			self.dragDirection = []
	def dragFunction(self):
		cmds.headsUpMessage( '    Value = ' + '  ' + str(self.attributeValue), time=0.1, verticalOffset=-100, horizontalOffset=-200 )
		dragPosition = cmds.draggerContext( 'dragTool', query=True, dragPoint=True)
		anchorPoint = cmds.draggerContext( 'dragTool', query =True, anchorPoint=True)
		#Finding the x and y distances Traveled
		x = ( ( dragPosition[0] - anchorPoint[0] ) * self.speed )
		y = ( ( dragPosition[1] - anchorPoint[1] ) * self.speed )
		z = ( ( dragPosition[2] - anchorPoint[2] ) * self.speed )
		# Start Building the List which figures out which way the mouse is traveling
		if len(self.dragDirection) < 3:
			self.dragDirection.append(dragPosition)
		# Once full we can calculate the direction
		else:
			X1 = self.dragDirection[0][0]; X2 = self.dragDirection[3-1][0]; xDist = abs(X2 - X1)
			Y1 = self.dragDirection[0][1]; Y2 = self.dragDirection[3-1][1];	yDist = abs(Y2 - Y1)
			Z1 = self.dragDirection[0][2]; Z2 = self.dragDirection[3-1][2];	zDist = abs(Z2 - Z1)
			# Find the max world distance traveled, is it X, Y or Z? Returns index and value
			worldDist = (abs(xDist), abs(yDist), abs(zDist))
			worldMax = max(worldDist)
			worldMaxIndex = worldDist.index(worldMax)
			worldMult = 10
			if self.space == 'screen':
				# X direction
				if X1 > X2:
					# negative
					xValue = abs(x) * -1
				else:
					# positive
					xValue = abs(x)
				if isinstance(self.attributeValue, list): # tests if attributeValue is a list or not ( for multiple values in one attr like: world scale )
					#print 'yes, is list'
					cmds.setAttr( self.attribute, self.attributeValue[0][0] + xValue, self.attributeValue[0][0] + xValue, self.attributeValue[0][0] + xValue)
				else:
					#print 'is not list'
					cmds.setAttr( self.attribute, self.attributeValue + xValue )
				cmds.refresh(currentView=True)
			elif self.space == 'world':
				if worldMaxIndex == 0: # X direction
					if X1 > X2:
						# negative
						worldValue = abs(x) * -1
					else:
						# positive
						worldValue = abs(x)
					cmds.setAttr( self.attribute, self.attributeValue[0][0] + (worldValue * worldMult), self.attributeValue[0][1], self.attributeValue[0][2] )
				if worldMaxIndex == 1: # Y direction
					if Y1 > Y2:
						# negative
						worldValue = abs(y) * -1
					else:
						# positive
						worldValue = abs(y)
					cmds.setAttr( self.attribute, self.attributeValue[0][0], self.attributeValue[0][1] + (worldValue * worldMult), self.attributeValue[0][2] )
				if worldMaxIndex == 2: # Z direction
					if Z1 > Z2:
						# negative
						worldValue = abs(z) * -1
					else:
						# positive
						worldValue = abs(z)
					cmds.setAttr( self.attribute, self.attributeValue[0][0], self.attributeValue[0][1], self.attributeValue[0][2] + (worldValue * worldMult) )
				cmds.refresh(currentView=True)
#pre-initialize tool
Dragger = DraggerTool()