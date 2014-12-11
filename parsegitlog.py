import commands
import re

pattern = re.compile(r'(commit .*\nAuthor: .*\nDate: .*\n)')

def ParseGitLog(log):
    match = pattern.split(log)
    if match:
        if match[0] == "":
            del match[0]
        Iscommit = True
        OneMessage = False
        AllMsg = []
	for i in range(len(match)):
            p = match[i]
            if Iscommit and p[:7] == "commit ":
                commit = p[7:47]
                commitbody = p
                Iscommit = False
            elif  (Iscommit == False) and (p[:7] != "commit "):
                body = p
                OneMessage = True
                Iscommit = True
            if OneMessage:
                Message = {'commit':commit,'body':commitbody + body}
                AllMsg.append(Message)
                OneMessage = False
    return AllMsg              
