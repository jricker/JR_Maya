class Refresh():
	def refreshAll(self):
		import JR_dragger_class
		import JR_attribute_class
		import JR_selection_class
		import JR_material_class
		import JR_camera_shake
		import JR_playblast_tool
		import JR_rename_tool
		import JR_camera_shuffle
		import JR_custom_window
		import JR_hud_class
		import JR_tool_class
		import JR_cache_class
		import JR_hk_cmds
		import JR_hk_map
		import JR_rename_class
		#######################
		reload(JR_dragger_class)
		reload(JR_attribute_class)
		reload(JR_selection_class)
		reload(JR_material_class)
		reload(JR_camera_shake)
		reload(JR_playblast_tool)
		reload(JR_rename_tool)
		reload(JR_camera_shuffle)
		reload(JR_custom_window)
		reload(JR_hud_class)
		reload(JR_tool_class)
		reload(JR_cache_class)
		reload(JR_hk_cmds)
		reload(JR_hk_map)
		reload(JR_rename_class)
RELOAD = Refresh()