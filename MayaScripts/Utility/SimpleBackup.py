# -*- coding:utf-8 -*-

import os, datetime, shutil
from maya.cmds import *

class SimpleBackup :
	sWndName = "SimpleBackupWnd"
	def __init__(self) :
		if window(self.sWndName, q=True, ex=True) :
			deleteUI(self.sWndName)
		wnd = window(
			self.sWndName,
			t = "Simple Backup"
		)
		lo = formLayout()
		af, ac, an = [], [], []
		self.memo = scrollField( editable=True, wordWrap=False, text="Dexcription..." )
		af += [(self.memo,"left",5), (self.memo,"right",5), (self.memo,"top",5)]
		btn = button(l="Backup", c=self.OnClicked_Backup)
		af += [(btn,"left",5), (btn,"right",5), (btn,"bottom",5)]
		an += [(btn,"top")]
		ac += [(self.memo,"bottom",5,btn)]
		setParent("..")
		formLayout(lo, e=True, af=af, ac=ac, an=an)
		showWindow(wnd)
	def OnClicked_Backup(self, *args) :
		scnName = file(q=True, loc=True)
		folder, name = os.path.split(scnName)
		name, ext = os.path.splitext(name)
		backupFolder = scnName + ".bck"
		if not os.path.exists(backupFolder) :
			os.mkdir(backupFolder)
		timestamp = datetime.datetime.now().strftime("_%y%m%d_%H%M")
		newName = name + timestamp + ext
		descName = name + timestamp + ".txt"
		shutil.copy(scnName, os.path.join(backupFolder, newName))
		try :
			fp = open(os.path.join(backupFolder, descName), "wt")
		except :
			print "error"
			return
		fp.write(scrollField(self.memo, q=True, tx=True))
		fp.close()
		deleteUI(self.sWndName)

SimpleBackup()