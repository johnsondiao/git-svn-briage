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
	def __init__(self, path):
		if False == self.IsValidPath(path):
			return False
		self.Path = path
		self.CmdPath = "cd " + self.Path + "; "
		mycmd = self.CmdPath + "git init"
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Git init Failed"
			return False
		IgnoreFile = open('.gitignore', 'w')
		IgnoreFile.write(".dg")
		IgnoreFile.close()
	def IsValidPath(self, path):
		if os.path.isdir(path) == False:
			return False
		if os.path.exists(path + "/.git"):
			return False
		return True
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
