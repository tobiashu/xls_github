#-*- coding:utf-8 -*-
import sys
from xml.etree import ElementTree

attrib_name = ['carrier', 'mcc', 'mnc', 'apn', 'proxy', 'port', 'mmsproxy', 'mmsport', 'mmsc', 'server', 'user', 'password', 'authtype', 'type']
output = ""

output_head = '''<?xml version="1.0" encoding="utf-8"?>
<apns version="7">
'''
output_tail = "</apns>\n"

def print_node(node):
	str_buff = "\t<apn "
	for name in attrib_name:
		if node.attrib.has_key(name) > 0:
			if 'carrier' == name:
			# replace < > & ' " with &lt; &gt; &amp; & apos; & quot;
				carrier_buff = ""
				for char in node.attrib[name]:
					if '<' == char:
						carrier_buff += "&lt;"
					elif '>' == char:
						carrier_buff += "&gt;"
					elif '&' == char:
						carrier_buff += "&amp;"
					elif '\'' == char:
						carrier_buff += "&apos;"
					elif '\"' == char:
						carrier_buff += "&quot;"
					else:
						carrier_buff += char
				str_buff += name+"=\"%s\" " % carrier_buff
			else:
				str_buff += name+"=\"%s\" " % node.attrib[name]
		else:
			str_buff += name+"=\"\" "			
	str_buff += "/>\n"
	output.write(str_buff)
		
# read xml 
def read_xml(text):
	root = ElementTree.fromstring(text)
	lst_node = root.getiterator("apn")
	output.write(output_head)
	for node in lst_node:
		print_node(node)
	output.write(output_tail)
		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage: apn_format.pyc [input_file] [output_file]"
	reload(sys)
	sys.setdefaultencoding( "utf-8" )	
	output = open(sys.argv[2],'wb')
	read_xml(open(sys.argv[1]).read())