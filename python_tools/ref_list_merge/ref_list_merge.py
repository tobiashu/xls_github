# -*- coding: utf-8 -*-
import string
import sys
import types
import xlrd
import xlwt


trans_count = 0
ref_count = 0
modify_count = 0

if len(sys.argv) <= 4:
	print "useage: ref_list_merge.py [ref_list_file] [translation_file] [output_file] [col_number]"
	print "for example: ref_list_merge.py ref_list_S601_CR.xls C7-translationg.xls output.xls L"
	exit(1)

trans_col = ord(sys.argv[4]) - ord('A')
#print trans_col
ref_book = xlrd.open_workbook(sys.argv[1])
ref_sh = ref_book.sheet_by_index(0)
trans_book = xlrd.open_workbook(sys.argv[2])
trans_sh = trans_book.sheet_by_index(0)

output_book = xlwt.Workbook(encoding = 'utf-8')
output_sheet = output_book.add_sheet('output_sheet', cell_overwrite_ok=True)


for rx in range(ref_count, ref_sh.nrows):
	ref_id = ref_sh.cell_value(rowx = rx, colx = 0)
	trans_id = trans_sh.cell_value(rowx = trans_count, colx = 0)
	output_sheet.write(rx, 0, ref_id)
	if ref_id == trans_id:
		trans_value = trans_sh.cell_value(rowx = trans_count, colx = trans_col)
		if type(trans_value) is not types.NoneType:	
			output_sheet.write(rx, trans_col, trans_value)
			trans_count = trans_count + 1
			ref_value = ref_sh.cell_value(rowx = rx, colx = trans_col)
			if ref_value != trans_value:
				modify_count = modify_count + 1
			continue
	ref_value = ref_sh.cell_value(rowx = rx, colx = trans_col)
	output_sheet.write(rx, trans_col, ref_value)

output_book.save(sys.argv[3])
print "Done!~ "
print str(modify_count) + " strings has been modified!"