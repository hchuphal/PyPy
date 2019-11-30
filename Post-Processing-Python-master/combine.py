#!/usr/bin/env python
#combineDL.py : Post Processing of TT Logs

import re
import os
import glob
import shutil 


#Function for dL CONFIG
def CombineDLConfig():
	infiles = glob.glob('*DL_Config.csv')
	outfilename="commonDL.csv"
	with open(outfilename, 'wb') as outfile:
#for filename in glob.glob('*.txt'):
		for filename in infiles:
			with open(filename, 'rb') as readfile:
				shutil.copyfileobj(readfile, outfile)

	input1  = open('commonDL.csv', 'r')
	headerdl= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'HpId' +', '+'CCE_Index' +', '+'AggLevel'  +', '+'TB0' +', '+'TB0_lcid'+' ,'+'TB0_size'+' ,'+'TB0_mcs'+', '+'TB1'+', '+'TB1_lcid'+' ,'+ 'TB1_size'+' ,'+'TB1_mcs'+', '+'nPrb Coding '+', '+'RI' +', '+'CQI' +', '+'HarqOffset '+'\n'
	with open('FinalDL.csv', 'a') as f2:
		f2.write(headerdl)
	output = open('FinalDL.csv', 'a')
	for line in input1:
		parts=line.split(',')
		times=re.sub("\D", "", parts[0])
		if times=='':
			continue
		output.write(line.replace(parts[0], times))

#Function for UL CONFIG
def CombineULConfig():
	infiles = glob.glob('*UL_Config.csv')
	outfilename="commonUL.csv"
	with open(outfilename, 'wb') as outfile:
#for filename in glob.glob('*.txt'):
		for filename in infiles:
			with open(filename, 'rb') as readfile:
				shutil.copyfileobj(readfile, outfile)

	input1  = open('commonUL.csv', 'r')
	headerul= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', '+'CCE_Index' +', '+'AggLevel' +', '+'RBs '+', '+'MCS' +', '+'Ndi' +', '+'TPC '+', '+' SNR'+', ' +'TargetSNR'+'\n'
	with open('FinalUL.csv', 'a') as f2:
		f2.write(headerul)
	output = open('FinalUL.csv', 'a')
	for line in input1:
		parts=line.split(',')
		times=re.sub("\D", "", parts[0])
		if times=='':
			continue
		output.write(line.replace(parts[0], times))



#Function for DL Harq
def CombineDLHarq():
	infiles = glob.glob('*DL_HARQ.csv')
	outfilename="commonDLHarq.csv"
	with open(outfilename, 'wb') as outfile:
#for filename in glob.glob('*.txt'):
		for filename in infiles:
			with open(filename, 'rb') as readfile:
				shutil.copyfileobj(readfile, outfile)

	input1  = open('commonDLHarq.csv', 'r')
	header_dl_harq='TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'H-PID'+', '+'numHarqTbs'+', '+'SFN'+', '+'SF'+', '+'HARQs Received: harq_status0'+','+'HARQs Received: harq_status1'+'\n'
	with open('FinalDLHarq.csv', 'a') as f2:
		f2.write(header_dl_harq)
	output = open('FinalDLHarq.csv', 'a')
	for line in input1:
		parts=line.split(',')
		times=re.sub("\D", "", parts[0])
		if times=='':
			continue
		output.write(line.replace(parts[0], times))


#Function for UL Harq
def CombineULHarq():
	infiles = glob.glob('*UL_HARQ.csv')
	outfilename="commonULHarq.csv"
	with open(outfilename, 'wb') as outfile:
#for filename in glob.glob('*.txt'):
		for filename in infiles:
			with open(filename, 'rb') as readfile:
				shutil.copyfileobj(readfile, outfile)

	input1  = open('commonULHarq.csv', 'r')
	header_ul_harq='TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'CRC_STATUS'+', '+'SFN'+', '+'SF'+', '+'current_tx_nb'+','+'max_num_tx'+'\n'
	with open('FinalULHarq.csv', 'a') as f2:
		f2.write(header_ul_harq)
	output = open('FinalULHarq.csv', 'a')
	for line in input1:
		parts=line.split(',')
		times=re.sub("\D", "", parts[0])
		if times=='':
			continue
		output.write(line.replace(parts[0], times))


#Function for DL LC STATS
def CombineDLlcStats():
	#Create Files for all UE Id
	outfiledlmetric='DL_LC_STATS.csv'
	infiles = 'InputDump.txt'
	uefile = open(infiles, 'r')	
	with open(outfiledlmetric, 'a') as f2:
			headerdlmetric= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'SfCnt' +', '+'LCID' +', '+'QCI'  +', '+'Weights' +', '+'mcs'+' ,'+'dl_scheduling Metric'+' ,'+'TP'+', '+'CurAlcn'+', '+'PRBsAvlbl'+' ,'+'TotalPendingData'+'\n'
			f2.write(headerdlmetric)
	for line in uefile:
		match1 = re.search('DL_LC_STATS:',line) #pattern avaialable in dump for DL_LC_STATS is #*#*
		with open(outfiledlmetric, 'a') as f2:
			if match1:
				pattern=line.split() # split line into parts
				size=len(pattern)
				if len(pattern) > 1:
					ts = pattern[1]
					sfn = pattern[3]
					sf=pattern[4]
					hsid = pattern[6]
					for i in range(6, size):
						if re.sub("\d", "", pattern[i])=='RNTI:':
							rnti=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='SfCnt:':
							SfCnt=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='LCID:':
							lcid=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='QCI:':
							qci=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='Wt:':
							wt=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='mcs:':
							mcs=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='M:':
							metric=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='TP:':
							tp=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='CurAlcn:':
							CurAlcn=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='PRBsAvlbl:':
							PRBsAvlbl=re.sub("\D", "", pattern[i])
						if re.sub("\d", "", pattern[i])=='TotalPendingData:-':
							TotalPendingData=re.sub("\D", "", pattern[i])
					datadlmetric= ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+SfCnt+', '+lcid +', '+qci+", "+wt+', '+mcs+', '+metric+', '+tp+', '+CurAlcn+', '+PRBsAvlbl+', '+TotalPendingData+', '+'\n'
					f2.write(datadlmetric)
					f2.flush()

#Function for uL LC STATS
def CombineULlcStats():
	 #Create Files for all UE Id
        outfileulmetric='UL_LC_STATS.csv'
        infiles = 'InputDump.txt'
	uefile = open(infiles, 'r')	
	#variable to check
	ul_m=0
	with open(outfileulmetric, 'a') as f2:
		headerulmetric= 'TimeStamp' +', '+ 'SFN'+', '+ ' SF '+', '+'HSID'+', '+'rnti' +', ' +'lcg_id' +', '+'Packets in_flight' +', '+'received'  +', '+'buffer_size' +', '+'lcg'+' ,'+'buffer_size'+' ,'+'metric'+', '+'Weights'+'\n'
		f2.write(headerulmetric)
	for line in uefile:
		match2 = re.search('get_ulsch_list',line)
		match3 = re.search('get_ulsch_list_ulmetric:',line)
		with open(outfileulmetric, 'a') as f2:
			if match3:
				pattern=line.split()
				size=len(pattern)
				for i in range(6, size):
					if re.sub("\d", "", pattern[i])=='lcg:':
						lcg=re.sub("\D", "", pattern[i])
					if re.sub("\d", "", pattern[i])=='buffer_size:':
						buffer_size=re.sub("\D", "", pattern[i])
					if re.sub("\d", "", pattern[i])=='metric:':
						metric=re.sub("\D", "", pattern[i])
					if re.sub("\d", "", pattern[i])=='W:':
						ul_w=re.sub("\D", "", pattern[i])
				ul_metirc=lcg+', '+buffer_size+', '+metric+', '+ul_w
				ul_m=1
			if match2:
				pattern=line.split() # split line into parts
				size=len(pattern)
				if len(pattern) > 1:
		    			ts = pattern[1]
					sfn = pattern[3]
					sf=pattern[4]
					hsid = pattern[6]
					for i in range(6, size):
						 if re.sub("\d", "", pattern[i])=='rnti:':
							 rnti=re.sub("\D", "", pattern[i])
						 if re.sub("\d", "", pattern[i])=='lcg_id:':
							 lcg_id=re.sub("\D", "", pattern[i])
						 if re.sub("\d", "", pattern[i])=='in_flight:':
							 in_flight=re.sub("\D", "", pattern[i])
						 if re.sub("\d", "", pattern[i])=='received:':
							 received=re.sub("\D", "", pattern[i])
						 if re.sub("\d", "", pattern[i])=='buffer_size:':
							 buffer_size=re.sub("\D", "", pattern[i])
					dataulmetric=ts+', '+sfn+', '+ sf+', '+hsid+', '+ rnti +', '+lcg_id+', '+in_flight +', '+received+", "+buffer_size
		   			if ul_m ==0:
						ul_metirc = '0' +','+'0'+', '+'0'+', '+'0'
					dataulm=dataulmetric+', '+ul_metirc+'\n'
					f2.write(dataulm)
					f2.flush()	

#Finally delete temo files
def delTemp():
        for file in os.listdir("./"):
                if file.startswith("common"):
                        os.remove(file)

if __name__ == '__main__':
        print "****Post Processing of DL Files File  "

