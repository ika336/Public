# -*- coding:utf-8 -*-

import os, re, shutil
from maya.cmds import *

class SimpleBackupRestore :
	sWndName = "SimpleBackupWnd"
	def __init__(self) :
		self.memoFiles = []
		if window(self.sWndName, q=True, ex=True) :
			deleteUI(self.sWndName)
		wnd = window(
			self.sWndName,
			t = "Simple Backup"
		)
		lo = formLayout()
		af, ac, an = [], [], []
		pan = paneLayout(cn="horizontal2")
		af += [(pan,"left",5), (pan,"right",5), (pan,"top",5)]
		self.lsFile = textScrollList(ams=False, sc=self.OnChanged_File)
		self.memo = scrollField( editable=False, wordWrap=False, text="" )
		setParent("..")
		btn = button(l="Restore", c=self.OnClicked_Restore)
		af += [(btn,"left",5), (btn,"right",5), (btn,"bottom",5)]
		an += [(btn,"top")]
		ac += [(pan,"bottom",5,btn)]
		setParent("..")
		formLayout(lo, e=True, af=af, ac=ac, an=an)
		if self.initUi() :
			showWindow(wnd)
		else :
			deleteUI(wnd)
	def initUi(self) :
		scnName = file(q=True, loc=True)
		folder, name = os.path.split(scnName)
		name, ext = os.path.splitext(name)
		backupFolder = scnName + ".bck"
		if not os.path.exists(backupFolder) :
			return False
		ptn = re.compile(".*_(\d{6})_(\d{4})")
		textScrollList(self.lsFile, e=True, ra=True)
		self.memoFiles = []
		for f in os.listdir(backupFolder) :
			n, e = os.path.splitext(f)
			if ".ma" != e and ".mb" != e : continue
			m = ptn.match(n)
			if not m : continue
			g1 = m.group(1)
			g2 = m.group(2)
			item = "'%s %s/%s %s:%s"%(g1[:2], g1[2:4], g1[4:], g2[:2], g2[2:])
			textScrollList(self.lsFile, e=True, a=item)
			self.memoFiles.append(os.path.join(backupFolder, n+".txt"))
		if 0 == textScrollList(self.lsFile, q=True, ni=True) :
			return False
		textScrollList(self.lsFile, e=True, sii=1)
		sMemo = ""
		try :
			fp = open(os.path.join(backupFolder, self.memoFiles[0]), "rt")
			sMemo = fp.read()
			fp.close()
		except :
			print "Faild to open .txt"
		scrollField(self.memo, e=True, tx=sMemo)
		return True
	def OnChanged_File(self, *args) :
		i = textScrollList(self.lsFile, q=True, sii=True)[0] -1
		sMemo = ""
		try :
			fp = open(self.memoFiles[i], "rt")
			sMemo = fp.read()
			fp.close()
		except :
			print "Faild to open .txt"
		scrollField(self.memo, e=True, tx=sMemo)
	def OnClicked_Restore(self, *args) :
		memoName = self.memoFiles[textScrollList(self.lsFile, q=True, sii=True)[0]-1]
		scnName = file(q=True, loc=True)
		folder, name = os.path.split(scnName)
		name, ext = os.path.splitext(name)
		backupName = memoName.replace(".txt", ext)
		shutil.copy(backupName, scnName)
		file(scnName, o=True)
		deleteUI(self.sWndName)

SimpleBackupRestore()