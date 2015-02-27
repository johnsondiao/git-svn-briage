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
	LastVersionFile = "/.svnlastversion.txt"
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
			self.GetLastVersion()
		else:
			print "This is not a svn workspace"
	def GetLastVersion(self):
		if self.Path != "":
			if os.path.exists(self.Path + self.LastVersionFile):
				versionfile = open(self.Path + self.LastVersionFile, "r")	
				LastVersion = versionfile.read()
				versionfile.close()
				if LastVersion[-1:] == '\n':
					LastVersion = LastVersion[:-1]
				return LastVersion
			else:
				if False == self.FreshLog():
					print "GetLastVersion Failed @ fresh log failed"
					return False
				else:
					self.WriteLastVersion(self.LogList[0]['head'][:])
					return self.LogList[0]['head'][:]
		else:
			print "GetLastVersion Failed @ no last version file"
			return False
	def WriteLastVersion(self, lastversion):
		if self.Path != "":
			versionfile = open(self.Path + self.LastVersionFile, "w")
			versionfile.write(lastversion)
			versionfile.close()		
			return True
		else:
			print "WriteLastVersion Failed"
			return False
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
		self.WriteLastVersion(self.LogList[0]['head'][:])
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
		if self.NewVersion == self.GetLastVersion():
			print "The Svn is the Newest"
			return True
		else:
			return False
	def CreatePatchOneVersion(self, path):
		OneStepIndex = 0
		for index in range(len(self.LogList)):
			if self.LogList[index]['head'] == self.GetLastVersion():
				break;
			OneStepIndex = index
		OneStepVersion = self.LogList[OneStepIndex]['head']
		patchfile = path + "/" + self.GetLastVersion() + "_" + OneStepVersion + ".patch"

		mycmd = self.CmdPath + "svn diff -r " + self.GetLastVersion()[1:] + ":" + OneStepVersion[1:] + ">" + patchfile
		err, ret = commands.getstatusoutput(mycmd)
		if 0!=err:
			print "Create path Failed:", ret
			return False, None
		self.WriteLastVersion(OneStepVersion)
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
		self.WriteLastVersion(self.LogList[0]['head'][:])
		return True
	
