import maya.cmds as cmds
import random
from JR_selection_class import *
class Materials(Selection):
	def __init__(self):
		pass
	def assignRandomMaterial(self, materialType = 'lambert', item = 'NA', materialName = 'NA', red = 'NA', green = 'NA', blue = 'NA'):
		# set conditions if nothing is specified in method call
		if item == 'NA':
			item = self.getSelection()
		if materialName == 'NA':
			materialName = 'tempMaterial_01'
		if red == 'NA':
			red = random.random()
		if green == 'NA':
			green = random.random()
		if blue == 'NA':
			blue = random.random()
		# start the process
		material = cmds.shadingNode(materialType, asShader=1, name= materialName)
		print material, ' this is the "material" data'
		SG = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name= materialName +'_SG')
		cmds.connectAttr((material +'.outColor'),(SG+'.surfaceShader'),f=1)
		cmds.setAttr(material+'.color', red, green, blue)
		cmds.sets(item, edit=1, forceElement=SG)