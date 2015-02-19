import os
import sys
from SvnObject import *
from GitObject import *
from sync import *
import pdb
class DgObject:
	path=""
	SvnObjectPath = ""
	GitObjectPath = ""
	def __init__(self):
		
	def Create(self, path):
		if os.path.exists(path + "/.dg"):
			print "This is already a Dg workspace"
			return False
		os.mkdir(path + "/.dg")
		self.path = path + "/.dg"
		self.SvnObjectPath = self.path + "/svn"
		self.GitObjectPath = self.path + "/git"
		os.mkdir(self.GitObjectPath)
		os.mkdir(self.SvnObjectPath)
		return True
	def Init(self, url):
		if self.path == "":
			print "Should Create Dg folder first"
			return False
		self.SvnObject = SvnObject(self.SvnObjectPath, url)
		if False == self.SvnObject:
			return False
		self.GitObject = GitObject(self.GitObjectPath)
		if False == self.GitObject:
			return False
		SyncDir(self.SvnObjectPath, self.GitObjectPath)	
		self.GitObject.Add();
		if False == self.GitObject.Commit(self.SvnObject.Logs):
			return False
	def Sync(self):
		'''first sync from svn to dg's git '''
		if False == self.SvnObject.Upload():
			print "Svn Upload Failed"
			return False
		if True == self.SvnObject.GotNew():
			print "This the Newest Svn workspace"
		
			
