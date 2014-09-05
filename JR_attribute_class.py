from JR_cache_class import *
import maya.cmds as cmds
class Attributes():
	def __init__(self):
		pass
	def setAttributes(self, attrs = ''):
		if attrs == '':
			Cache.currentAttribute = ''
		else:
			Cache.currentAttribute = attrs[0][1]
		Cache.attributeList = attrs
		Cache.offset = 0 # reset offset
		self.updateAttrHUD()
	def switchAttribute(self):
		if Cache.offset > len(Cache.attributeList)-1:
			Cache.offset = 0
			return Cache.attributeList[Cache.offset] [1] # 1 is for the second value in the tuple
		elif Cache.offset < 0:
			Cache.offset = len(Cache.attributeList)-1
			return Cache.attributeList[Cache.offset] [1]  # 1 is for the second value in the tuple
		else:
			#attribute = self.history[-1] + attributes[Cache.offset]
			return Cache.attributeList[Cache.offset] [1]  # 1 is for the second value in the tuple
	def attr_toggleUp(self):
		Cache.offset +=1
		Cache.currentAttribute = self.switchAttribute()
		self.updateAttrHUD()
	def attr_toggleDown(self):
		Cache.offset -=1
		Cache.currentAttribute = self.switchAttribute()
		self.updateAttrHUD()
	def updateAttrHUD(self):
		cmds.headsUpDisplay( 'currAttrHUD', edit = True, c =  self.setCurrentHUD )
		cmds.headsUpDisplay( 'nextAttrHUD', edit = True, c =  self.setNextHUD )
		cmds.headsUpDisplay( 'prevAttrHUD', edit = True, c =  self.setPreviousHUD )
	def setCurrentHUD(self):
		if Cache.attributeList == '':
			return ''
		else:
			return Cache.attributeList[Cache.offset] [0] # 0 is used to access the name instead of the value
	def setNextHUD(self):
		if Cache.attributeList == '':
			return ''
		else:
			if Cache.offset == len(Cache.attributeList)-1:
				return Cache.attributeList[0] [0]
			else:
				return Cache.attributeList[Cache.offset+1] [0]
	def setPreviousHUD(self):
		if Cache.attributeList == '':
			return ''
		else:
			return Cache.attributeList[Cache.offset-1] [0]