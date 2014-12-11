import os
import sys
import shutil
import commands
import re
from parsesvnlog import *

pattern = re.compile(r'[-]*\nr\d* \| [^\|]*\|[^\|]*\|[^\|-]*')
 
def errExit(msg):
    print "-" * 50
    print "ERROR:"
    print msg
    sys.exit(1)
 
def GetSvnLog(source_dir):
    print "Get the log from", source_dir
    mycmd = "cd " + source_dir + ";svn log"
    err, log = commands.getstatusoutput(mycmd)
    AllMsg =  ParseSvnLog(log)
    print AllMsg
    return AllMsg
if __name__ == "__main__":
    if len(sys.argv) != 2:
        if "-h" in sys.argv or "--help" in sys.argv:
            print __doc__
            sys.exit(1)
        errExit(u"invalid arguments!")
    source_dir = sys.argv[1]
    if os.path.isdir(source_dir) == False:
        errExit(u"'%s' is not a folder!" % source_dir)
 
    GetSvnLog(source_dir)
