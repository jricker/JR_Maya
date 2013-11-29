class myCache():
	def __init__(self):
		self.attributeList = []
		self.offset = 0
		self.keyOffset = 0
		self.currentTool = ''
		self.currentCategory = ''
		self.currentAttribute = ''
		self.currentContext = ''
		self.faceSelection = ''
		self.edgeSelection = ''
		self.vertSelection = ''
		self.jointSelection = ''
		self.meshSelection = ''
		# cached for picture in picture feature
		self.cameraJob = 2000
		self.modelPanel = ''
		self.camSceneOffset = 0
		self.camDefaultOffset = 0
		self.lensHUDvis = 0
		# cached items for playblast settings
		self.playblastFormat = 'qt'
		self.playblastSize = [1280, 720]
		self.playblastCodec = 'Sorenson Video 3'
		self.playblastLocation = ''
Cache = myCache()