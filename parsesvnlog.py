import re
import pdb
pattern = re.compile(r'([ ]*[-]*\n[ ]*r\d* \| [^\|]*\|[^\|]*\|[^\|\n]*)')
 
def ParseSvnLog(log):
	match = pattern.split(log)
	for i in range(len(match)):
		if match[0].find("----------") == -1:
			del match[0] 	
	IsHead = True
	OneMessage = False
	AllMsg = [] 
	for i in range(len(match)):
		p = match[i]
		if IsHead and (p.find("----------") != -1):
			if re.search(r'r\d*', p) != None:
				head = re.search(r'r\d*', p).group()
				headbody = p
				IsHead = False
		elif i != len(match) and (IsHead == False) and (p.find("----------") == -1):
			body = p
			OneMessage = True
			IsHead = True
		elif (IsHead == False) and i == (len(match) - 1):
			body = p.split('\n---')[0]
			OneMessage = True
			IsHead = True
		if OneMessage:
			Message = {'head':head, 'body':headbody + body}
			AllMsg.append(Message)
			OneMessage = False
	return AllMsg
