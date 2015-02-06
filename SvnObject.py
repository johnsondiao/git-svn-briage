import os
import sys
import commands
import pdb

class SvnObject:
	Path = ""
	Log = ""
        
	def __init__(self, path):
		IsValidPath(path)
	def IsValidPath(self, path):
		if os.path.isdir(path) == False:
			return False
		mycmd = "cd " + path + "; svn log"
		err, self.Log = commands.getstatusoutput(mycmd)
		pdb.set_trace()

