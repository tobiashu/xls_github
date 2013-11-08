import os
import Image
import glob
import re
cwd = os.getcwd()
gif_files = glob.glob('*.gif')
jpg_files = glob.glob('*.jpg')
bmp_files = glob.glob('*.bmp')
def img2code(files):
	for file in files:
		fr = open(file, 'rb')
		fw = open(file.replace('.','_') + '.h','w')
		imgsize = os.path.getsize(file)
		im=Image.open(file)
		imw=list(im.size)[0]
		imh=list(im.size)[1]
		fw.write("{\n\t")
		fw.write(imgtype(file),)
		fw.write("0x%02X, " %(imgsize&0xff),)
		fw.write("0x%02X, " %((imgsize>>8)&0xff),)
		fw.write("0x%02X, " %((imgsize>>16)&0xff),)
		fw.write("0x%02X, " %(imh&0xff),)
		fw.write("0x%02X, " %(((imh>>8)&0x0f)|(imw&0x0f)<<4),)
		fw.write("0x%02X,\n\t" %(imw>>4))
		i = 0
		temp = ''
		while fr.tell() != imgsize:
			temp = fr.read(1)
			fw.write("0x%02s," % temp.encode('hex').upper(),)
			i = i + 1
			if i == 16:
				i = 0
				fw.write("\n\t")
			else:
				fw.write(" ")
		fw.write("\n}")
		fr.close()
		fw.close()
def imgtype(file):
	m_gif = re.findall(r'\.gif$',file.lower())
	m_jpg = re.findall(r'\.jpg$',file.lower())
	m_bmp = re.findall(r'\.bmp$',file.lower())
	if m_gif:
		return "0x03, 0x01, "
	elif m_jpg:
		return "0x09, 0x01, "
	elif m_bmp:
		return "0x04, 0x01, "
	else:
		assert(0)
img2code(gif_files)
img2code(jpg_files)
img2code(bmp_files)
