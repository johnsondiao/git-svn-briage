import os
import sys
import commands
import pdb
from parsesvnlog import *
class SvnObject:
	Path = ""
	Logs = ""
	LogList = ""
        CmdPah = ""
	LastVersion = ""
	def __init__(self, path = None):
		'''the path has svn'''	
		if path == None:
			return
		if os.path.isdir(path) == False:
			print "This is not a folder"
			return
		if path[-3:] == "svn":
			self.Path = path
			self.CmdPath = "cd " + self.Path + "; "
			if False == self.FreshLog():
				return 
			self.LastVersion = self.LogList[0]['head'][:]
		else:
			print "This is not a svn workspace"
	def Create(self, path, url):
		'''the path is the parent of svn workspace'''
		if os.path.isdir(path) == False:
			print "This is not a folder"
			return False
		if os.path.exists(path + "/svn"):
			print "This is already a svn workspace"
			return False
		os.mkdir(path + "/svn")
		self.Path = path + "/svn"
		self.CmdPath = "cd " + self.Path + "; "
		mycmd = self.CmdPath + "svn checkout " + url + " " + self.Path;
		print "Checkout svn from ", url, " to ", self.Path 
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Checkout Failed err ", err, " status ", ret
			return False
		if False == self.FreshLog():
			return False
		self.LastVersion = self.LogList[0]['head'][:]
		return True
	def FreshLog(self):
		mycmd = self.CmdPath + "svn log"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Get svn log Failed err", err, " status ",ret
			return False
		self.Logs = ret
		self.LogList = ParseSvnLog(self.Logs)
		return True	
	def Update(self):
		mycmd = self.CmdPath + r'svn update'
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Svn upload Failed ret", ret
			return False
		else:
			if False == self.FreshLog():
				return False
			return True
		return False
	def IsNewest(self):
		if False == self.FreshLog():
			print "Get Log Failed"
			return 

		self.NewVersion = self.LogList[0]['head'][:]
		if self.NewVersion == self.LastVersion:
			print "The Svn is the Newest"
			return True
		else:
			return False
	def CreatePatchOneVersion(self, path):
		OneStepIndex = 0
		for index in range(len(self.LogList)):
			print "index ", index
			if self.LogList[index]['head'] == self.LastVersion:
				break;
			OneStepIndex = index
		OneStepVersion = self.LogList[OneStepIndex]['head']
		patchfile = path + "/" + self.LastVersion + "_" + OneStepVersion + ".patch"

		mycmd = self.CmdPath + "svn diff -r " + self.LastVersion[1:] + ":" + OneStepVersion[1:] + ">" + patchfile
		err, ret = commands.getstatusoutput(mycmd)
		if 0!=err:
			print "Create path Failed:", ret
			return False, None
		self.LastVersion = OneStepVersion
		return True, patchfile, self.LogList[OneStepIndex]['body']
		
	def ApplyPatch(self, patchfile):
		mycmd = self.CmdPath + "patch -p0 <" + patchfile
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print ret
			return False
		return True
	def Commit(self, log):
		mycmd = self.CmdPath + r'svn commit -m "' + log + r'"'
		err, ret = commands.getstatusoutput(mycmd)
		if 0!= err:
			print "Failed to Commit svn log"
			return False
		mycmd = self.CmdPath + "svn update"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Failed to update svn"
			return False
		if False == self.FreshLog():
			return False
		self.LastVersion = self.LogList[0]['head'][:]
		return True
	
