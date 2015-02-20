import os
import sys
from SvnObject import *
from GitObject import *
from sync import *
import pdb
class DgObject:
	Path=""
	SvnObjectPath = ""
	GitObjectPath = ""
	def __init__(self, path = None):
		'''This path has .dg '''
		if path == None:
			return
		if False == os.path.isdir(path):
			print "This is not a folder"
			pdb.set_trace()
			return
		if path[-3:] == ".dg":
			self.Path = path
			self.SvnObjectPath = self.Path + "/svn"
			self.GitObjectPath = self.Path + "/git"
			self.GitObject = GitObject(self.GitObjectPath)
			self.SvnObject = SvnObject(self.SvnObjectPath)
		else:
			print "There is no .dg under path", path

	def Create(self, path, url):
		'''The path is the parents of .dg.'''
		if False == os.path.isdir(path):
			print "This is not a folder"
			return False
		if os.path.exists(path + "/.dg"):
			print "This is already a Dg workspace"
			return False
		os.mkdir(path + "/.dg")
		self.Path = path + "/.dg"
		self.SvnObject = SvnObject()
		if False == self.SvnObject.Create(self.Path, url):
			return False
		self.GitObject = GitObject()
		if False == self.GitObject.Create(self.Path):
			return False
		self.SvnObjectPath = self.SvnObject.Path
		self.GitObjectPath = self.GitObject.Path
		SyncDir(self.SvnObjectPath, self.GitObjectPath)	
		self.GitObject.Add();
		if False == self.GitObject.Commit(self.SvnObject.Logs):
			return False
	def SyncFromSvn(self):
		'''first sync from svn to dg's git '''
		if False == self.SvnObject.Update():
			print "Svn Upload Failed"
			return False
		while False == self.SvnObject.IsNewest():	
			err, patchfile, patchlog = self.SvnObject.CreatePatchOneVersion(self.Path)
			if False == err:
				print "Create patch Failed"
				return False
			err = self.GitObject.ApplyPatch(patchfile, patchlog)
			if False == err:
				print "Apply patch Failed"
				return False
			os.remove(patchfile)
				
	def PushToSvn(self):
		'''push to svn from dg's git'''
		while False == self.GitObject.IsNewest():
			err, patchfile,patchlog = self.GitObject.CreatePatchOneVersion(self.Path)
			if False == err:
				print "Create patch Failed:"
				return False
			err = self.SvnObject.ApplyPatch(patchfile)
			if False == err:
				print "Apply patch Failed"
				return False
			err = self.SvnObject.Commit(patchlog)
			if False == err:
				print "Commit Failed"
				return False
			os.remove(patchfile)	
