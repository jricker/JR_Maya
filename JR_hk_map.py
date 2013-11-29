import maya.cmds as cmds
from functools import partial
from JR_cache_class import *
class Mapping():
	def __init__(self):
		pass
	def globalHotkeys(self):
		# ~
		cmds.nameCommand('tilde', ann= 'tilde', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.tilde()\")")
		cmds.nameCommand('alt_tilde', ann= 'alt_tilde', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_tilde()\")")
		cmds.nameCommand('ctrl_tilde', ann= 'ctrl_tilde', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.ctrl_tilde()\")")
		# 1
		cmds.nameCommand('one', ann= 'one', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.one()\")")
		cmds.nameCommand('alt_one', ann= 'alt_one', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_one()\")")
		# 2
		cmds.nameCommand('two', ann= 'two', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.two()\")")
		cmds.nameCommand('alt_two', ann= 'alt_two', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_two()\")")
		# 3
		cmds.nameCommand('three', ann= 'three', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.three()\")")
		cmds.nameCommand('alt_three', ann= 'alt_three', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_three()\")")
		# 4
		cmds.nameCommand('alt_four', ann= 'alt_four', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_four()\")")
		# Q
		cmds.nameCommand('q', ann= 'q', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.q()\")")
		cmds.nameCommand('q_release', ann= 'q_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.q_release()\")")
		# W
		cmds.nameCommand('w', ann= 'w', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.w()\")")
		cmds.nameCommand('w_release', ann= 'w_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.w_release()\")")
		# E
		cmds.nameCommand('e', ann= 'e', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.e()\")")
		cmds.nameCommand('e_release', ann= 'e_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.e_release()\")")
		# R
		cmds.nameCommand('r', ann= 'r', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.r()\")")
		cmds.nameCommand('ctrl_r', ann= 'ctrl_r', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.ctrl_r()\")")
		cmds.nameCommand('r_release', ann= 'r_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.r_release()\")")
		cmds.nameCommand('alt_r', ann= 'alt_r', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_r()\")")
		# L
		cmds.nameCommand('ctrl_l', ann= 'ctrl_l', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.ctrl_l()\")")
		# P
		cmds.nameCommand('alt_p', ann= 'alt_p', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_p()\")")
		cmds.nameCommand('alt_p_release', ann= 'alt_p_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_p()\")")
		# F
		cmds.nameCommand('F', ann= 'F', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.F()\")")
		# B
		cmds.nameCommand('alt_b', ann= 'alt_b', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_b()\")")
		# D
		cmds.nameCommand('d', ann= 'd', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.d()\")")
		# I
		cmds.nameCommand('i', ann= 'i', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.i()\")")
		cmds.nameCommand('alt_i', ann= 'alt_i', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_i()\")")
		cmds.nameCommand('ctrl_i', ann= 'ctrl_i', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.ctrl_i()\")")
		# O
		cmds.nameCommand('o', ann= 'o', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.o()\")")
		# C
		cmds.nameCommand('c', ann= 'c', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.c()\")")
		cmds.nameCommand('c_release', ann= 'c_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.c_release()\")")
		cmds.nameCommand('alt_c', ann= 'alt_c', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_c()\")")
		cmds.nameCommand('alt_shift_c', ann= 'alt_shift_c', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_shift_c()\")")
		# V
		cmds.nameCommand('v', ann= 'v', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.v()\")")
		cmds.nameCommand('v_release', ann= 'v_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.v_release()\")")
		# X
		cmds.nameCommand('x', ann= 'x', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.x()\")")
		cmds.nameCommand('x_release', ann= 'x_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.x_release()\")")
		# S
		cmds.nameCommand('S', ann= 'S', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.S()\")")
		cmds.nameCommand('alt_s', ann= 'alt_s', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_s()\")")
		cmds.nameCommand('ctrl_S', ann= 'ctrl_S', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.ctrl_S()\")")
	def categoryHotkeys(self):
		# X
		cmds.nameCommand(Cache.currentCategory + '_alt_x', ann= Cache.currentCategory + '_alt_x', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_x()\")")
		# C
		cmds.nameCommand(Cache.currentCategory + '_C', ann= Cache.currentCategory + '_C', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.C()\")")
		cmds.nameCommand(Cache.currentCategory + '_C_release', ann= Cache.currentCategory + '_C_release', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.C_release()\")")
		# E
		cmds.nameCommand(Cache.currentCategory + '_alt_e', ann= Cache.currentCategory + '_alt_e', stp='python', c="python(\"from JR_hk_cmds import *;i=Hotkeys();i.alt_e()\")")

	################################################################################################################################
	def displayCategory(self):
		return Cache.currentCategory.upper()
	def setCategory(self, category):	
		Cache.currentCategory = category # set hotkey category to selected
		self.categoryHotkeys() # intializes the nameCommands
		cmds.headsUpDisplay('categoryHUD', edit=True, c = self.displayCategory ) # update HUD with hotkey category
		# GLOBAL HOTKEYS
		# `
		cmds.hotkey( k='`', name= 'tilde' ) # tilde
		cmds.hotkey( k='`', alt=True, name= 'alt_tilde' ) # Alt + tilde
		cmds.hotkey( k='`', ctl=True, name= 'ctrl_tilde' ) # Ctrl +  tilde
		# 1
		cmds.hotkey( k='1', name= 'one' ) # one
		cmds.hotkey( k='1', alt=True, name= 'alt_one' ) # Alt + one
		# 2
		cmds.hotkey( k='2', name= 'two' ) # two
		cmds.hotkey( k='2', alt=True, name= 'alt_two' ) # Alt + two
		# 3
		cmds.hotkey( k='3', name= 'three' ) # three
		cmds.hotkey( k='3', alt=True, name= 'alt_three' ) # Alt + three
		# 4
		cmds.hotkey( k='4', alt=True, name= 'alt_four' ) # Alt + four
		# Q
		cmds.hotkey( k='q', name= 'q', releaseName = 'q_release' ) # q
		# W
		cmds.hotkey( k='w', name= 'w', releaseName = 'w_release' ) # w
		# E
		cmds.hotkey( k='e', name= 'e', releaseName = 'e_release' ) # e
		# R
		cmds.hotkey( k='r', name= 'r', releaseName = 'r_release' ) # r
		cmds.hotkey( k='r', ctl=True, name = 'ctrl_r' ) # Ctrl + r
		cmds.hotkey( k='r', alt=True, name = 'alt_r' ) # Alt + r
		# L
		cmds.hotkey( k='l', ctl=True, name = 'ctrl_l' ) # Ctrl + l
		# P
		cmds.hotkey( k='p', alt=True, name = 'alt_p', releaseName = 'alt_p_release' ) # Alt + p
		# F
		cmds.hotkey( k='F', name= 'F' ) # F
		# B
		cmds.hotkey( k='b', alt=True, name= 'alt_b' ) # ctrl + b
		# D
		cmds.hotkey( k='d', name= 'd' ) # d
		# I
		cmds.hotkey( k='i', name= 'i' ) # i
		cmds.hotkey( k='i', alt=True, name= 'alt_i' ) # Alt + i
		cmds.hotkey( k='i', ctl=True, name= 'ctrl_i' ) # Ctrl + i
		# O
		cmds.hotkey( k='o', name= 'o' ) # o
		# C
		cmds.hotkey( k='c', name= 'c', releaseName = 'c_release') # c
		cmds.hotkey( k='c', alt=True, name= 'alt_c') # alt + c
		cmds.hotkey( k='C', alt=True, name= 'alt_shift_c') # alt + shift + c
		# V
		cmds.hotkey( k='v', name= 'v', releaseName = 'v_release') # v
		# CATEGORY HOTKEYS
		# X
		cmds.hotkey( k='x', name= 'x', releaseName = 'x_release') # x
		cmds.hotkey( k='x', alt=True, name= category + '_alt_x' ) # Alt + x
		# C
		cmds.hotkey( k='C', name= category + '_C', releaseName = 'C_release' ) # Shift + c
		# E
		cmds.hotkey( k='e', alt=True, name= category + '_alt_e' ) # Alt + e
		# S
		cmds.hotkey( k='S', name= 'S' ) # S
		cmds.hotkey( k='s', alt=True, name= 'alt_s' ) # Alt + s
		cmds.hotkey( k='S', ctl=True, name= 'ctrl_S' ) # Ctrl + Shift + s
#
Map = Mapping()