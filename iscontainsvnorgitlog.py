from parsegitlog import *
from parsesvnlog import *

import pdb

def IsGitLogInSvnLogS(SvnLogS):
	for i in range(len(SvnLogS)):
		GitLogBodyParse = ParseGitLog(SvnLogS[i]['body'])
		if GitLogBodyParse != []:
			return i, GitLogBodyParse
	return -1, []

def IsSvnLogInGitLogS(GitLogS):
	for i in range(len(GitLogS)):
		SvnLogBodyParse = ParseSvnLog(GitLogS[i]['body'])
		if SvnLogBodyParse != []:
			return i, SvnLogBodyParse
	return -1, []
