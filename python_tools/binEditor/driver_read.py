# -*- coding: utf-8 -*-

def read_driver(filename):
	f = open(filename, 'rb')
	f2 = open(r'lcd.drv', 'wb')
	i = 0
	temp = ""
	while temp != "xls-lcd:":
		i = i + 1
		f.seek(i)
		temp = f.read(8)
	index = 0
	while temp != "drv-end;":
		f.seek(i)
		temp = f.read(1)
		if len(temp) == 0:
			break
		else:
			f2.write(temp)
			print "%3s" % temp.encode('hex'),
			index = index + 1
		if index == 4:
			index = 0
			print
		temp = f.read(8)
		i = i + 1
	f.close()
	f2.close()

if __name__ == "__main__":
	read_driver(r'a.out')

