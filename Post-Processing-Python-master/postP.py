#!/usr/bin/env python
#postP.py : Post Processing of TT Logs

import sys
import re
import os
def postProcessing(uniques):
	print "*********Logs Post Processing \n"   
	totalUes=0
	tb0=tb1=0
	#Create Files for each UE Id
	dl_config=updateCqi=ul_snr=ul_config=ul_m=0
	for item in uniques :
		uefile = open(item+'.in', 'r')
		outfiledl=item+'_DL_Config.csv'
		outfileul=item+'_UL_Config.csv'
		outfiledlhq=item+'_DL_HARQ.csv'
		outfileulhq=item+'_UL_HARQ.csv'
		with open(outfiledl, 'a') as f2:
			headerdl= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'HpId' +', '+'TPC'+', '+'CCE_Index' +', '+'AggLevel'  +', '+'TB0' +', '+'TB0_lcid'+' ,'+'TB0_size'+' ,'+'TB0_mcs'+', '+'TB1'+', '+'TB1_lcid'+' ,'+ 'TB1_size'+' ,'+'TB1_mcs'+', '+'nPrb Coding '+', '+'RI' +', '+'CQI' +', '+'HarqOffset '+'\n'
			dl_harq='TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'H-PID'+', '+'numHarqTbs'+', '+'HARQs Received: harq_status1'+','+'HARQs Received: harq_status1'+'\n'
			f2.write(headerdl)
		with open(outfileul, 'a') as f2:
			headerul= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', '+'CCE_Index' +', '+'AggLevel' +', '+'RBs '+', '+'MCS' +', '+'Ndi' +', '+'TPC '+', '+' SNR'+', ' +'TargetSNR'+'\n'
			#print header
			f2.write(headerul)
		with open(outfiledlhq, 'a') as f2:
			header_dl_harq='TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'H-PID'+', '+'numHarqTbs'+', '+'SFN'+', '+'SF'+', '+'HARQs Received: harq_status0'+','+'HARQs Received: harq_status1'+'\n'
			f2.write(header_dl_harq)
		with open(outfileulhq, 'a') as f2:
			header_ul_harq='TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'CRC_STATUS'+', '+'SFN'+', '+'SF'+', '+'current_tx_nb'+','+'max_num_tx'+'\n'
			f2.write(header_ul_harq)
	
		for line in uefile:
		#if any(s in line for s in strings):
		#if any(s in line for s in strings):
						
			match1 = re.search('updateWidebandCqiPucch:pd', line)
			match2 = re.search('DL_CONFIG_REQ_DATA',line)
			match3 = re.search('DCI0_CONFIG_REQ',line)
			match4 = re.search('UL_SNR_UPDATE',line)
			match5 = re.search('DL_HARQ_STATUS',line)
			match6 = re.search('UL_CRC_HANDLE',line)
			#match7 = re.search('#*#*',line) #pattern avaialable in dump for DL_LC_STATS is #*#*
			#match8 = re.search('get_ulsch_list:',line)
			#match9 = re.search('get_ulsch_list_ulmetric:',line)
			
			#match7 = re.search('DL_TRANMISSION_RATE',line)
			#match8 = re.search('HARQ_RETX_STATUS',line)
			#match8 = re.search('LC_TP',line)
			#match9 = re.search('DCI_INFO',line)
			#match11 = re.search('DL_PRB_UTILIZATION',line)
			match10 = re.search('LC_SCH',line)
		 
			with open(outfiledl, 'a') as f2:
				#if line == searchquery:
				if match1:
					pattern=line.split() # split line into parts
					size=len(pattern)
					for i in range(6, size):
						if re.sub("\d", "", pattern[i])=='ri:':
							ri=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='wb_cqi:' or re.sub("\d", "", pattern[i])==':wb_cqi:':
							cqi=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='HarqOff:':
							harqOff=re.sub("\D", "", pattern[i])
					updateCqi=1
					datacqi=ri+','+cqi+','+harqOff
				#	if (dl_config==1 or updateCqi==1):
				#		if(len(data) >0):
				#			outdata = data +','+datacqi+ '\n'
				#			f2.write(outdata)
				#			#f2.flush()
				#	else:
				#		dl_config=updateCqi=0
				if match2:
					#print " Check One"
					tb0=tb1=0
					pattern=line.split() # split line into parts
					size=len(pattern)
					if len(pattern) > 1:
						#print line
						#print pattern[4],pattern[9],pattern[12],pattern[14]
						ts = pattern[1]
						sfn = pattern[3]
						sf=pattern[4]
						hsid = pattern[6]
						for i in range(6, size):
							if re.sub("\d", "", pattern[i])=='RNTI:':
								rnti=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='H-PID:':
								hpid=re.sub("\D", "", pattern[i])
								#print hpid
							if re.sub("\d", "", pattern[i])=='tpc:':
								tpc=re.sub("\D", "", pattern[i])
								
							if re.sub("\d", "", pattern[i])=='cce_index:':
								re.sub("\d", "", pattern[i])
								cceIndex=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='aggr_level:':
								agglevel=re.sub("\D", "", pattern[i])
							#print rnti
								str(rnti)
							rbC=pattern[i]
							tempstr=re.sub("\d", "", rbC)
							if tempstr[:9]=='rb_coding':
								p=rbC.split(':')
								if(len(p)>1):
									rb=p[1]
									str(rb)
							#else:
							#	rb ="Invalid Value in Dump"
							if pattern[i]=='TB0':
								tb0='1'
								tb0_lcid=re.sub("\D", "", pattern[i+1])
								tb0_size=re.sub("\D", "", pattern[i+2])
								tb0_mcs=re.sub("\D", "", pattern[i+3])
								tb1=tb1_lcid=tb1_mcs=tb1_size='0'
								str(tb0)
								str(tb0_mcs)
								str(tb0_lcid)
								str(tb0_size)
								if tb0!='1':
									tb0=tb0_lcid=tb0_mcs=tb0_size=rb='0'
												
							if pattern[i]=='TB1':
								tb1='1'
								tb1_lcid=re.sub("\D", "", pattern[i+1])
								tb1_size=re.sub("\D", "", pattern[i+2])
								tb1_mcs=re.sub("\D", "", pattern[i+3])
								str(tb1)
								str(tb1_mcs)
								str(tb1_lcid)
								str(tb1_size)
								if tb1 !='1':
									tb1=tb1_lcid=tb1_mcs=tb1_size=rb='0'
							if tb1==0:
								tb1=tb1_lcid=tb1_mcs=tb1_size=rb='0'
						if updateCqi==0:
							datacqi='0'+', '+'0'+', '+'0'	
						datadl= ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+ hpid +', '+tpc+', '+cceIndex+', '+agglevel+' ,'+tb0+', '+tb0_lcid+' ,'+tb0_size+' ,'+tb0_mcs+' ,'+tb1+', '+tb1_lcid+' ,'+tb1_size+' ,'+tb1_mcs+' ,'+rb#+'\n' #+'\n' #+','+rb+','+ri+','+cqi+','+harqOff+ '\n'
						outdata = datadl +','+datacqi+ '\n'
						f2.write(outdata)
					#	f2.write(data)
#						dl_config=1
	
			with open(outfileul, 'a') as f2:
				#if line == searchquery:
			#for UL SNR pattern
				if match4:
					pattern=line.split()
					size=len(pattern)
					for i in range(6, size):
						if re.sub("\d", "", pattern[i])=='SNR:':
							snr=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='target_snr:':
							targertSINR=re.sub("\D", "", pattern[i])
					dataSNR=snr+', '+targertSINR
					ul_snr=1
					#if (ul_config==1 or ul_snr==1):
					#	if(len(dataul) >0) and ul_snr==1:
					#		uloutdata = dataul +','+dataSNR+ '\n'
					#		f2.write(uloutdata)
					#		f2.flush()
					#else:
					#	ul_config=ul_snr=0
				
				if match3:
					pattern=line.split() # split line into parts	
					size=len(pattern)
					if len(pattern) > 1:
						#print pattern[4],pattern[9],pattern[12],pattern[14]
						ts1 = pattern[1]
						ts = pattern[1]
						sfn = pattern[3]
						sf=pattern[4]
						hsid = pattern[6]
						for i in range(6, size):
							if re.sub("\d", "", pattern[i])=='RNTI:':
								rnti=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='cce_index:':
								cceIndex=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='aggr_level:':
								agglevel=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='cce_index:':
								cceIndex=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='num_rb:':
								rbs=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='mcs:':
								mcs=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='ndi:':
								ndi=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='tpc:':
								tpc=re.sub("\D", "", pattern[i])
						
						dataul= ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+ cceIndex +', '+agglevel+" ,"+rbs+", "+mcs+", "+ndi+", "+tpc
						if ul_snr ==0:
							dataSNR = '0' +','+'0'
						uloutdata = dataul +','+dataSNR+ '\n'
						f2.write(uloutdata)
						f2.flush()
			#for UL SNR pattern
				
			with open(outfiledlhq, 'a') as f2:
			#if line == searchquery:
				if match5:
				#print " Check One"
					pattern=line.split() # split line into parts
					size=len(pattern)
					if len(pattern) > 1:
					#print line
					#print pattern[4],pattern[9],pattern[12],pattern[14]
						ts = pattern[1]
						sfn = pattern[3]
						sf=pattern[4]
						hsid = pattern[6]
						for i in range(6, size):
							if re.sub("\d", "", pattern[i])=='UE:':
								rnti=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='H-PID::':
								temp=re.sub("\D", "", pattern[i])
								str(temp)
								hpid=temp[:1]
								numHarqTbs=temp[-1:]
							if re.sub("\d", "", pattern[i])=='SFN:':
								SFN=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='SF:':
								SF=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='[DTX|DTX]':
								#rnti=re.sub("\D", "", pattern[i])
								harq_status0='DTX'
								harq_status1='DTX'
							if re.sub("\d", "", pattern[i])=='[DTX|ACK]':
								#rnti=re.sub("\D", "", pattern[i])
								harq_status0='DTX'
								harq_status1='ACK'
							if re.sub("\d", "", pattern[i])=='[DTX|NACK]':
								#rnti=re.sub("\D", "", pattern[i])
								harq_status0='DTX'
								harq_status1='NACK'
							if re.sub("\d", "", pattern[i])=='[NACK|DTX]':
								#rnti=re.sub("\D", "", pattern[i])
								harq_status0='NACK'
								harq_status1='DTX'
							if re.sub("\d", "", pattern[i])=='[ACK|DTX]':
								harq_status0='ACK'
								harq_status1='DTX'
							if re.sub("\d", "", pattern[i])=='[ACK|ACK]':
								harq_status0='ACK'
								harq_status1='ACK'
							if re.sub("\d", "", pattern[i])=='[ACK|NACK]':
								harq_status0='ACK'
								harq_status1='NACK'
							if re.sub("\d", "", pattern[i])=='[NACK|NACK]':
								harq_status0='NACK'
								harq_status1='NACK'
							if re.sub("\d", "", pattern[i])=='[NACK|ACK]':
								harq_status0='NACK'
								harq_status1='ACK'
							if re.sub("\d", "", pattern[i])=='[ACK]':
								harq_status0='ACK'
								harq_status1='NA'
							if re.sub("\d", "", pattern[i])=='[NACK]':
								harq_status0='NACK'
								harq_status1='NA'
							if re.sub("\d", "", pattern[i])=='[DTX]':
								harq_status0='DTX'
								harq_status1='NA'
						datadlhq= ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+ hpid +', '+numHarqTbs+" ,"+SFN+", "+SF+', '+harq_status0+', '+harq_status1+', '+'\n'
						f2.write(datadlhq)
						f2.flush()
			with open(outfileulhq, 'a') as f2:
				#if line == searchquery:
				if match6:
				#print " Check One"
					pattern=line.split() # split line into parts
					size=len(pattern)
					if len(pattern) > 1:
						#print line
						#print pattern[4],pattern[9],pattern[12],pattern[14]
						ts = pattern[1]
						sfn = pattern[3]
						sf=pattern[4]
						hsid = pattern[6]
						#temp=pattern[10]
						string=re.sub("\D", "", pattern[10])
						#print string
						str(string)
						sizesf=len(string)
						SFN=string[:sizesf-1]
						SF=string[-1:]
						#print line
						#print size
						#print pattern[i]
						for i in range(6, size):
							if re.sub("\d", "", pattern[i])=='rnti:':
								rnti=re.sub("\D", "", pattern[i])
						#	print pattern[i]
					#	print re.sub("\d", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='Good':
								crc_status='1'
							if re.sub("\d", "", pattern[i])=='Bad':
								crc_status='0'
							if re.sub("\d", "", pattern[i])=='current_tx_nb:':
								current_tx_nb=re.sub("\D", "", pattern[i])
							if re.sub("\d", "", pattern[i])=='max_num_tx:':
								max_num_tx=re.sub("\D", "", pattern[i])
						dataulhq= ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+ crc_status +', '+SFN+", "+SF+', '+current_tx_nb+', '+max_num_tx+', '+'\n'
						f2.write(dataulhq)
						f2.flush()
					
			with open(outfiledl, 'a') as f2:
				if match10:
					pattern=line.split() # split line into parts
					size=len(pattern)
					if len(pattern) > 1:
						ts = pattern[1]
						sfn = pattern[3]
						sf=pattern[4]
						hsid = pattern[6]
			
			
if __name__ == '__main__':
        print "\n ****Calling Post Processing for each UE********\n"
		#print "\n***** Processing TT Dump File : %s ****** "% filename 
