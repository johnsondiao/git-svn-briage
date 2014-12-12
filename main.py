#!/usr/bin/python
from sync import *
from getgitlog import *
from getsvnlog import *
from parsegitlog import *
import commands

def main(svn_dir, git_dir):
	err, upinfo = commands.getstatusoutput("cd " + svn_dir + ";svn up")
	if err != 0:
		print "svn up failed"
		return
	if not ("At revision" in upinfo):
		print "svn up wrong:", upinfo
		return
	SvnLogS = GetSvnLog(svn_dir)
	if len(SvnLogS) == 0:
		return
	print SvnLogS[0]['body']
	SvnLogBodyParse = ParseGitLog(SvnLogS[0]['body'])
	if SvnLogBodyParse != []:
		print "TODO"
		return
	else:
		GitLogS = GetGitLog(git_dir)
		print GitLogS
	#SyncDir(git_dir, svn_dir)

		


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
	main(svn_dir, git_dir)
