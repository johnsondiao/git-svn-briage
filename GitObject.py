import os
import sys
import commands
import pdb
from parsesvnlog import *
from parsegitlog import *
class GitObject:
	Path = ""
	Logs = ""
	LogList = ""
        CmdPath = ""
	Name = ""
	def __init__(self, path = None, name = None):
		'''this path include the folder name'''
		if name == None:
			name = "/git"
		if path == None:
			return
		if False == os.path.isdir(path):
			print "This is not a folder"
			return
		if path[-len(name):] == name:
			self.Path = path
			self.CmdPath = "cd " + self.Path + "; "
			if False == self.FreshLog():
				return
			self.LastVersion = self.LogList[0]['commit'][:]
		else:
			print "There is no git workspace"
	def Create(self, path, name = None):
		'''This path is the parent path of git workspace'''
		if name == None:
			self.Name = "/git"
		else:
			self.Name = "/" + name
		if False == os.path.isdir(path):
			print "This is not a folder"
			return False
		if os.path.exists(path + self.Name):
			print "This is already a git workspace, path + self.Name =", path+self.Name
			return False
		os.mkdir(path + self.Name)
		self.Path = path + self.Name
		self.CmdPath = "cd " + self.Path + "; "
		mycmd = self.CmdPath + "git init"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Git init Failed"
			return
	def FreshLog(self):
		mycmd = self.CmdPath + "git log"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Get git log Faield:",ret
			return False
		self.Logs = ret
		self.LogList = ParseGitLog(self.Logs)
		return True
	def IsNewest(self):
		if False == self.FreshLog():
			return
		self.NewVersion = self.LogList[0]['commit'][:]
		if self.NewVersion == self.LastVersion:
			print "The Git is the Newest"
			return True
		else:
			return False
	def CreatePatchOneVersion(self, path):
		OneStepIndex = 0
		for index in range(len(self.LogList)):
			print "index ", index
			if self.LogList[index]['commit'] == self.LastVersion:
				break
			OneStepIndex = index
		OneStepVersion = self.LogList[OneStepIndex]['commit']
		patchfile = path + "/" + self.LastVersion + "_" + OneStepVersion + ".patch"
		mycmd = self.CmdPath + "git diff --no-prefix " + self.LastVersion + " " + OneStepVersion + ">" + patchfile
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Create patch failed:", ret
			return False, None
		self.LastVersion = OneStepVersion
		return True, patchfile, self.LogList[OneStepIndex]['body']	


	def Add(self):
		mycmd = self.CmdPath + "git add ."
		commands.getstatusoutput(mycmd)
		return True
	def Commit(self, log):
		self.Add()
		print "git commit ", log
		mycmd = self.CmdPath + r'git commit -a -m "' + log + r'"'
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Failed to commit git log"
			return False
		if False == self.FreshLog():
			return False
		self.LastVersion = self.LogList[0]['commit'][:]	
		return True
	def Pull(self, path):
		mycmd = self.CmdPath + r'git pull ' + path;
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Git Pull Failed err ", err, "ret ", ret
			return False
		return True	
	def ApplyPatch(self, patchfile, patchlog):
		mycmd = self.CmdPath + "git apply " + patchfile;
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print ret
			return False
		return self.Commit(patchlog)
