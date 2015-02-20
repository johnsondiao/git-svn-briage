import os
import sys
import commands
import pdb
from parsesvnlog import *
class GitObject:
	Path = ""
	Logs = ""
	LogList = ""
        CmdPah = ""
	def __init__(self, path = None):
		'''this path has git'''
		if path == None:
			return
		if False == os.path.isdir(path):
			print "This is not a folder"
			return
		if path[-3:] == "git":
			self.Path = path
			self.CmdPath = "cd " + self.Path + "; "
		else:
			print "There is no git workspace"
	def Create(self, path):
		'''This path is the parent path of git workspace'''
		if False == os.path.isdir(path):
			print "This is not a folder"
			return False
		if os.path.exists(path + "/git"):
			print "This is already a git workspace"
			return False
		os.mkdir(path + "/git")
		self.Path = path + "/git"
		self.CmdPath = "cd " + self.Path + "; "
		mycmd = self.CmdPath + "git init"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Git init Failed"
			return
	def Add(self):
		mycmd = self.CmdPath + "git add ."
		commands.getstatusoutput(mycmd)
		return True
	def Commit(self, log):
		mycmd = self.CmdPath + r'git commit -a -m "' + log + r'"'
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Failed to commit git log"
			return False
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
