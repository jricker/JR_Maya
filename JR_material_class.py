import maya.cmds as cmds
import random
from JR_selection_class import Selection
class Materials(Selection):
	def __init__(self):
		pass
		#Selection.__init__(self)
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
	def assignTestMaterial(self, materialType = 'lambert', item = 'NA', materialName = 'NA'):
		# variables
		filePath = self.userFolder + '/Copy/ASSETS/TEXTURES/__Default/uv_grid_01.jpg'
		# set conditions if nothing is specified in method call
		if item == 'NA':
			item = self.getSelection()
		if materialName == 'NA':
			materialName = 'testMaterial'
		# check to see if it already exists
		sceneShaders = cmds.ls(materials = True)
		shaderExists = [i for i in sceneShaders if materialName in i]
		print shaderExists, ' THIS IS THE SHADER TEST LIST'
		if shaderExists == []:
			#create a shader
			material = cmds.shadingNode(materialType, asShader=1, name= materialName)
			file_node=cmds.shadingNode("file",asTexture=True, name=materialName + '_image')
			SG = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name= materialName +'_SG')
			cmds.connectAttr((material +'.outColor'),(SG+'.surfaceShader'),f=1)
			cmds.connectAttr(file_node +'.outColor', material + '.color')
			cmds.setAttr('testMaterial_image.fileTextureName', filePath, type='string')
			cmds.sets(item, edit=1, forceElement=SG)
		else:
			# assign the shader
			cmds.sets(item, edit=True, forceElement= materialName+'_SG')				