#!python 2.7
import re
import sys
#useage: type "rf_auto_gen.py [input file name] [output file name]" in cmd line
f = open(sys.argv[1])
fw = open(sys.argv[2],'w')
lines = f.readlines()

start_loss_of_gain_flag = 0
start_power_ramp_flag = 0
max_arf_cn = {}
rx_loss = {}
apc_lowest_power = 0
subband_max_arfcn = {}
subband_mid_level = {}
subband_high_weight = {}
subband_low_weight = {}
battery_weight = {}

for line in lines:
	match = re.findall(r'\[(.*?)\]', line)
	if match:		
		#calibration data for loss of gain
		m = re.findall(r'(.*?) Sub band, RX loss', match[0])
		if m:
			if start_loss_of_gain_flag == 0:
				start_loss_of_gain_flag = 1
				print "Calibration data for path loss of gain ... ..."
				fw.write("/*----------------------------------------*/\n")
				fw.write("/* Calibration data for path loss of gain */\n")
				fw.write("/*----------------------------------------*/\n\n")
			#print m[0]
			fw.write("/* ")
			fw.write(m[0])
			fw.write("....................................................................*/\n\n")
			fw.write("sAGCGAINOFFSET  AGC_PATHLOSS_")
			fw.write(m[0])
			fw.write("[ PLTABLE_SIZE ] =\n{")

			#Calibration data for power ramp 
		m = re.findall(r'(.*?) level, ramp',match[0])
		if m:
			if start_power_ramp_flag == 0:
				start_power_ramp_flag = 1
				print "Calibration data for power ramp ... ..."
				fw.write("/*----------------------------------------*/\n")
				fw.write("/* Calibration data for power ramp        */\n")
				fw.write("/*----------------------------------------*/\n\n")
			fw.write("/* ")
			fw.write(m[0])
			fw.write("....................................................................*/\n\n")
			fw.write("sRAMPDATA  ")
			fw.write(m[0])
			fw.write("_RampData =\n{\n   /*-------------------------------------------------------------------------------------------*/\n")
	else:
		match = re.split(r'=', line)
		if match[1]:
			#Calibration data for path loss of gain
			if match[0] == 'Max ARFCN':
				max_arf_cn = re.split(r',', match[1])
			if match[0] == 'RX loss':
				rx_loss = re.split(r',', match[1])
				counter = 0
				for i in max_arf_cn:
					if rx_loss[counter][0] == '-':
						j = rx_loss[counter][:6]
					else:
						j = rx_loss[counter][:5]
					fw.write('\t{ ' + "{0}, GAINLOSS( {1:>3} )".format(i.strip('\n'), j) + ' },\n')	
					counter = counter + 1
				max_arf_cn = {}
				rx_loss = {}
				fw.write('	/*-------------------------*/\n	{ TABLE_END }\n};\n\n')
				
			#Calibration data for power ramp 
			if match[0] == 'APC dc offset':
				apc_dc_offset = match[1]
			if match[0] == 'APC lowest power':
				apc_lowest_power = match[1]
				fw.write('   /* lowest power */\n   ((%s)<<8) | %s,\t/*APC_DC_OFFSET = %s*/\n' %(apc_dc_offset[0],apc_lowest_power[0], apc_dc_offset[0]))
				fw.write("   /*-------------------------------------------------------------------------------------------*/\n")
				fw.write("   /* power level  */\n")
				fw.write('   /*  ')
				for n in range(0, 15):
					fw.write('%d, ' %(n * 2 + int(apc_lowest_power[0])))
					n = n + 1
				fw.write('%d dBm                        */\n' %(n * 2 + int(apc_lowest_power[0])))
			if match[0] == 'TX power level':
				fw.write('   { ' + match[1][:-1] + '},\n')
				fw.write('   /*-------------------------------------------------------------------------------------------*/\n')
				fw.write('   {\n')
				
			m = re.findall(r'profile (\d+) ramp up',match[0])
			if m:
				temp_str = "      /* profile {0:>2} :{1:>3} dBm | p00,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12,p13,p14,p15  */\n".format(m[0], int(apc_lowest_power[0]) + 2 * int(m[0]))
				fw.write(temp_str)
				m = re.split(r',', match[1])
				fw.write('      {  /* ramp up   */ {  {')
				for i in m[:-1]:
					fw.write("{0:>3},".format(i))
				fw.write("{0:>3}".format(m[-1][:-1]))
				fw.write(' },\n')
				
			m = re.findall(r'profile (\d+) ramp down',match[0])	
			if m:
				fw.write('         /* ramp down */    { ')
				m = re.split(r',', match[1])
				for i in m[: -1]:
					fw.write("{0:>3},".format(i))
				fw.write("{0:>3}".format(m[-1][:-1]))	
				fw.write(' }  }\n')
				fw.write('      }, /*-------------------------------------------------------------------------------------*/\n')
			
			if match[0] == 'Subband max arfcn':
				fw.write('   },\n')
				fw.write('   /* ARFCN WEIGHT */\n')
				fw.write('   {  /* max arfcn , mid_level ,  hi_weight   ,  lo_weight   */\n')
				subband_max_arfcn = re.split(r',', match[1])	
				
			if match[0] == 'Subband mid level':
				subband_mid_level = re.split(r',', match[1])
			
			if match[0] == 'Subband high weight':
				subband_high_weight = re.split(r',', match[1])
			
			if match[0] == 'Subband low weight':
				subband_low_weight = re.split(r',', match[1])
				num = 0
				for i in subband_max_arfcn:
					temp_line = "{0}    ,    {1}     , WEIGHT({2}), WEIGHT({3})".format(i.strip('\n'), subband_mid_level[num].strip('\n'), subband_high_weight[num][:7], subband_low_weight[num][:7])
					fw.write('      {       ')
					fw.write(temp_line)
					fw.write('},\n')
					num = num + 1
				fw.write('      /*------------------------------------------------------*/\n      { TABLE_END }\n   },\n')	
				#reset sub band data
				subband_max_arfcn = {}
				subband_mid_level = {}
				subband_high_weight = {}
				subband_low_weight = {}

			if match[0] == 'Battery compensate, low voltage, low temperature':
				battery_weight[0] = match[1]
			if match[0] == 'Battery compensate, low voltage, mid temperature':
				battery_weight[1] = match[1]
			if match[0] == 'Battery compensate, low voltage, high temperature':
				battery_weight[2] = match[1]
			if match[0] == 'Battery compensate, mid voltage, low temperature':
				battery_weight[3] = match[1]
			if match[0] == 'Battery compensate, mid voltage, mid temperature':
				battery_weight[4] = match[1]
			if match[0] == 'Battery compensate, mid voltage, high temperature':
				battery_weight[5] = match[1]
			if match[0] == 'Battery compensate, high voltage, low temperature':
				battery_weight[6] = match[1]
			if match[0] == 'Battery compensate, high voltage, mid temperature':
				battery_weight[7] = match[1]
			if match[0] == 'Battery compensate, high voltage, high temperature':
				battery_weight[8] = match[1]
				fw.write('   /* Battery WEIGHT */\n   {  /*      low temp,       mid temp,        hi temp */\n')
				fw.write('       {  ' + 'WEIGHT({0}),  WEIGHT({1}),  WEIGHT({2})'.format(battery_weight[0][:5],battery_weight[1][:5],battery_weight[2][:5]) + '  },  /* low volt */\n')
				fw.write('       {  ' + 'WEIGHT({0}),  WEIGHT({1}),  WEIGHT({2})'.format(battery_weight[3][:5],battery_weight[4][:5],battery_weight[5][:5]) + '  },  /* mid volt */\n')
				fw.write('       {  ' + 'WEIGHT({0}),  WEIGHT({1}),  WEIGHT({2})'.format(battery_weight[6][:5],battery_weight[7][:5],battery_weight[8][:5]) + '  },  /* hi volt */\n\t},\n};\n\n\n')			
f.close()
fw.close()
print "finished!"
	