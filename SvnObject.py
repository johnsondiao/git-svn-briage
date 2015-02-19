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
	def __init__(self, path, url):
		if False == self.IsValidPath(path):
			return False
		if False == self.Checkout(url):
			return False
	def IsValidPath(self, path):
		if os.path.isdir(path) == False:
			return False
		if os.path.exists(path + "/.svn"):
			return False
		self.Path = path
		self.CmdPath = "cd " + self.Path + "; "
	def Checkout(self, url):
		mycmd = self.CmdPath + "svn checkout " + url + " " + self.Path;
		print "Checkout svn from ", url, " to ", self.Path 
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Checkout Failed err ", err, " status ", ret
			return False
		if False == self.FreshLog():
			return False
		self.LastVersion = self.LogList[0]['head'][1:]
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
	def Upload(self):
		mycmd = self.CmdPath + r'svn upload'
		err, ret = commands.getstatusoutput(mycmd)
		if 0 != err:
			print "Svn upload Failed"
			return False
		else:
			if False == self.FreshLog():
				return False
			return True
		return False
	def GotNew(self):
		newversion = self.LogList[0]['head'][1:]
		if newversion == self.LastVersion:
			print "The Svn is the Newest"
			return False
		else:
			self.LastVersion = newversion
			return True
		
		
