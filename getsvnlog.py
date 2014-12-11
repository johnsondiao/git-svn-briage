import os
import sys
import shutil
import commands
import re

pattern = re.compile(r'/[-]*r\d* \| [^\|]*\|[^\|]*\|[^\n]*/')
 
def errExit(msg):
    print "-" * 50
    print "ERROR:"
    print msg
    sys.exit(1)
 
def main(source_dir):
    print "Get the log from", source_dir
    mycmd = "cd " + source_dir + ";svn log"
    #err, log = commands.getstatusoutput(mycmd)
    err = 0
    log = ""
    print "err = ", err
    print "log = ", log
    NextCommitBegin = 0
    AllMsg = []
    if not err:
 #       while (NextCommitBegin != -1):    
            match = pattern.match(log)
            if match:
                print match.group()
            
'''
            CommitBegin = log.find("commit ", NextCommitBegin)
            CommitBodyBegin = CommitBegin + 7
            CommitBodyEnd = CommitBodyBegin + 40
            NextCommitBegin = log.find("commit ", CommitBodyEnd)
            if NextCommitBegin == -1:
                Body = log[CommitBegin :]
            else:
                Body = log[CommitBegin : NextCommitBegin]
            Commit = log[CommitBodyBegin : CommitBodyEnd]
            Message = {'Commit': Commit,'Body': Body}
            AllMsg.append(Message)
    return AllMsg
   ''' 
 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        if "-h" in sys.argv or "--help" in sys.argv:
            print __doc__
            sys.exit(1)
        errExit(u"invalid arguments!")
    source_dir = sys.argv[1]
    if os.path.isdir(source_dir) == False:
        errExit(u"'%s' is not a folder!" % source_dir)
 
    main(source_dir)
