import re

pattern = re.compile(r'([-]*\nr\d* \| [^\|]*\|[^\|]*\|[^\|-]*)')
 
def ParseSvnLog(log):
	match = pattern.split(log)
	if match:
		if match[0] == "":
			del match[0]
		IsHead = True
		OneMessage = False
		AllMsg = [] 
		for i in range(len(match)):
			p = match[i]
			if IsHead and p[:10] == "----------":
				head = re.search(r'r\d*', p).group()
				headbody = p
				IsHead = False
			elif (IsHead == False) and (p[:10] != "----------"):
				body = p
				OneMessage = True
				IsHead = True
			if OneMessage:
				Message = {'head':head, 'body':headbody + body}
				AllMsg.append(Message)
				OneMessage = False
	return AllMsg
