#!/usr/bin/python
from sync import *
from getgitlog import *
from getsvnlog import *
from parsegitlog import *
import commands

def CreateGitFromSvn(svn_dir, git_dir):
	err, lsInfo = commands.getstatusoutput("cd " + git_dir + "; ls -a")
	if ".git" in lsInfo:
		print "The git dir is not  empty:", git_dir
		return -1


	SyncDir(svn_dir, git_dir)
	err, InitInfo = commands.getstatusoutput("cd " + git_dir + "; git init")
	if err != 0:
		print "git init failed"
		return -1
	if "Initialized empty Git repository" in InitInfo:
		print "Create Git repository succeed"
	else:
		print "Create Git repository failed:", InitInfo
		return -1
	err, AddInfo = commands.getstatusoutput("cd " + git_dir + "; git add .")
	if err != 0:
		print "git add failed"
		return -1
	err, SvnLogS = commands.getstatusoutput("cd " + svn_dir + "; svn log")
	if err != 0:
		print "svn log failed"
		return -1
	err, GitCommit = commands.getstatusoutput("cd " + git_dir + "; git commit -a -m \"" + SvnLogS + "\"")
	if err != 0:
		print "git commit failed"
		return -1
			

if __name__ == "__main__":
	if len(sys.argv) != 3:
		if "-h" in sys.argv or "--help" in sys.argv:
			print __doc__
			sys.exit(1)
		errExit(u"invalid arguments!")
	svn_dir = sys.argv[1]
	git_dir = sys.argv[2]
	if os.path.isdir(svn_dir) == False:
		errExit(u"'%s' is not a folder!" % svn_dir)
	if os.path.isdir(git_dir) == False:
		errExit(u"'%s' is not a folder!" % git_dir)
	CreateGitFromSvn(svn_dir, git_dir)
