#!/usr/bin/env python
#Main.py : Post Processing of brcm logger Logs

import re
import sys
import os

#Dump Analysis for res.txt logs
def Process_InputDump(fileProcess,euCount):
        try :
                file = open(fileProcess, 'r')
        except IOError:
                print "Error: can\'t find file or read data"
        else:
                #print "Opened in the file %s successfully" %fileProcess
                lines = file.readlines()
                file.close()
        print " **** Checking for all ELs in the Log.... *** "
	infile = fileProcess
        outfilename="ELs.csv"
        headerdl= ', '+ 'SFN'+', '+ ' SF '+', '+'Start::MAC TC(us)'+', '+'Stop::MAC TC(us)' +', ' +'MAC TC(us)' +', '+'Start:Encode(us)' +', '+'Stop:Encode(us)'  +', '+'Enocde(us)' +', '+'Start:MAC_NTC(us)'+' ,'+'Stop:MAC_NTC(us)'+' ,'+'MAC_NTC(us)'+'\n'
        with open(outfilename,'a') as f2:
                f2.write(headerdl)
	resfile = open(infile, 'r') 
	diff1=diff2=diff3=s1=m1=m2=m3=m4=m5=m6=0
	SYSFRAMENUM=SUBFRAME=0
	for line in resfile:
                #if any(s in line for s in strings):
			sfnsf = re.search('payload', line)
			#sfnsf = re.search('0x0000', line)
                        match1 = re.search('111100', line)
                        match2 = re.search('111114',line)
                        match3 = re.search('222200',line)
                        match4 = re.search('222203',line)
                        match5 = re.search('111114',line)
                        match6 = re.search('111128',line)
                        with open(outfilename, 'a') as f2:
				if match2:
					m2=1
                                        pattern=line.split() # split line into parts
                               		size=len(pattern)
                                        mac_stopT=pattern[9]
					#mac_stop = [ float(re.sub("[^0-9.]", " ", x)) for x in mac_stopT]
					mac_stop=re.findall("\d+.\d+", mac_stopT)
				if sfnsf:
					s1=1	
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
					for i in range(6, size):
						#if re.sub("\d", "", pattern[i])=='0x000019':
						if  '0x0000' in pattern[i]:
							tempValue = re.sub("\D", "", pattern[18])
							sfnsfV=int(tempValue)
                                        		SYSFRAMENUM=(((sfnsfV) & 0xFFF0) >> 4)
							str(SYSFRAMENUM)
                                        		SUBFRAME= ( (sfnsfV) & 0x000F)
							str(SUBFRAME)
                                if match1:
					m1=1
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
					mac_startT=pattern[9]
					#mac_start=re.sub("\D", "", pattern[9])
					mac_start=re.findall("\d+.\d+", mac_startT)
					#print mac_start

				if (m1 == 1 & m2==1):
					diff1=float(mac_stop[0]) - float (mac_start[0])
					str(mac_start[0])
					str(mac_stop[0])
					str(diff1)
				if match3:
					m3 = 1
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
                                        encode_startT=pattern[9]
                                        #encode_start=re.sub("\D", "", pattern[9])
					encode_start=re.findall("\d+.\d+", encode_startT)
				if match4:
					m4=1
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
                                        encode_stopT=pattern[9]
                                       # encode_stop=re.sub("\D", "", pattern[10])
					encode_stop=re.findall("\d+.\d+", encode_stopT)
				if (m3 == 1 & m4 ==1):
					diff2=float(encode_stop[0]) - float (encode_start[0])
					str(diff2)
					str(encode_start[0])
					str(encode_stop[0])
				if match5:
					m5=1
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
                                        macnct_startT=pattern[9]
					macnct_start=re.findall("\d+.\d+", macnct_startT)
                                        #macnct_start=re.sub("\D", "", pattern[9])
				if match6:
					m6=1
                                        pattern=line.split() # split line into parts
                                        size=len(pattern)
                                        macnct_stopT=pattern[9]
					macnct_stop=re.findall("\d+.\d+", macnct_stopT)
                                        #macnct_stopt=re.sub("\D", "", pattern[9])
				if (m5 == 1 & m6 ==1):
					diff3=float(macnct_stop[0]) - float(macnct_start[0])
					str(diff3)
					str(macnct_start[0])
					str(macnct_stop[0])
				if (m1 & m6):
					dataEL= ' ,'+str(SYSFRAMENUM) +','+ str(SUBFRAME) +','+ mac_start[0] +',' + mac_stop[0] +','+ str(diff1) +' us'+',' + encode_start[0] +','+ encode_stop[0] +','+ str(diff2)+' us'+ ','+ macnct_start[0] +',' + macnct_stop[0]+','+ str(diff3)+' us' + '\n'
					s1=m1=m2=m3=m4=m5=m6=0
					diff1=diff2=diff3=0
					SYSFRAMENUM=SUBFRAME=mac_start[0]=mac_stop[0]=encode_start[0]=encode_stop[0]=macnct_start[0]=macnct_stop[0]="NA"
        				f2.write(dataEL)
	
def Logs_Files():
        for file in os.listdir("./"):
                if file.endswith(".csv") or file.endswith(".in"):
                        os.remove(file)
                
        #print "\n************ Removed all Previous Logs! *************"
        # listing directories
        #print "The dir is: %s \n "%os.listdir(os.getcwd())

#List All OutPut Files
def ListFiles():
        #print "All Logs files Generated as .csv per MAC ELs  :"
        for file in os.listdir("./"):
                if file.endswith(".csv"):
                        print "Output File : ",file, "\n"


if __name__ == '__main__':
        if len(sys.argv)<2:
                print "\nPlease Provide Input Files ..Calling exit!!"
                print '  Usage : main.py  <inputfile> \n \n'
                sys.exit(2)
        print " \n****Post Processing of Input File  >> %s: " % sys.argv[1]

        #Calling LogFiles To Remove Log Files
        Logs_Files()

        #Process Dump from read_logger
        Process_InputDump('res.txt',0)
        print "****Post Processing Successfully Completed >> Els.csv "
        #List All OutPut Files
        ListFiles()

#end
