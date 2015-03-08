import xml.etree.ElementTree as ET
import os
import pdb
class CheckListFile:
	def __init__(self, filepath = None):
		if filepath != None:
        		if os.path.isfile(filepath):
        			self.Tree = ET.parse(filepath)
        			self.Root = self.Tree.getroot()
	def Create(self, filepath):
		self.File = filepath
		if os.path.exists(filepath) == False:
			root = ET.Element(filepath.replace("/", "").replace(".", "").replace("-", ""))
			tree = ET.ElementTree(root)
			tree.write(filepath, encoding="utf-8")
	        self.Tree = ET.parse(filepath)
	        self.Root = self.Tree.getroot()
		return True
	def SetElement(self, layer0, layer1, layer2 = None):
		if layer2 == None:
			et = self.Root.find(layer0)
			if et == None:
				ET.SubElement(self.Root, layer0)
				et = self.Root.find(layer0)
			et.text = layer1
		elif layer0 != None and layer1 != None and layer2 != None:
			first = self.Root.find(layer0)
			if first == None:
				ET.SubElement(self.Root, layer0)
				first = self.Root.find(layer0)
			second = first.find(layer1)
			if second == None:
				ET.SubElement(first, layer1)
				second = first.find(layer1)
			second.text = layer2
		self.Tree.write(self.File, encoding="utf-8")
	def AddElement(self, layer0, layer1, layer2 = None):
		if layer2 == None:
			sub = ET.SubElement(self.Root, layer0)
			sub.text = layer1
		elif layer0 != None and layer1 != None and layer2 != None:
			first = self.Root.find(layer0)
			if first == None:
				ET.SubElement(self.Root, layer0)
				first = self.Root.find(layer0)
			sub = ET.SubElement(first, layer1)
			sub.text = layer2
		self.Tree.write(self.File, encoding="utf-8")		
	def RemoveElement(self, layer0, layer1 = None, layer2 = None):
		if layer1 == None and layer2 == None:
			for sub in self.Root.findall(layer0):
				self.Root.remove(sub)
		else:
			for first in self.Root.findall(layer0):
				if layer2 == None:
					first.remove(layer1)
				else:
					for second in first.findall(layer1):
						if second.text == layer2:
							first.remove(second)

		
		self.Tree.write(self.File, encoding="utf-8")
		return
	def GetElement(self, layer0, layer1 = None, layer2 = None):
		retlist = []
		for first in self.Root.findall(layer0):
			second = ""
			if layer2 == None and layer1 == None:
				retlist.append(first.text)
			elif layer2 == None and layer1 != None:
				for second in first.findall(layer1):
					retlist.append(second.text)
			elif layer2 != None and layer1 != None:
				for third in second.findall(layer2):
					retlist.append(third.text)
		return retlist		
os.remove(os.getcwd() + "/test.xml")
if __name__ == '__main__':
	test = CheckListFile()
	test.Create(os.getcwd() + "/test.xml")
	test.SetElement("layer0", "0")
	test.AddElement("layerA", "A")
	print test.GetElement("layer0")
	test.SetElement("layer0", "layer1", "1")
	test.AddElement("layer0", "layer1", "2")
	print test.GetElement("layer0", "layer1")
	test.RemoveElement("layer0", "layer1", "2")
	test.RemoveElement("layer0")

		
		 
