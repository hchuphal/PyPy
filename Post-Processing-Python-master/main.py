#!/usr/bin/env python
#Main.py : Post Processing of TT Logs

import re
import sys
import os
import postP
import LogFiles
import align
import combine

	
#Dump Analysis for UEs starts
def Process_InputDump(fileProcess,euCount):
	try :
		file = open(fileProcess, 'r')
	except IOError:
		print "Error: can\'t find file or read data"
	else:
		print "Opened in the file %s successfully" %fileProcess
		lines = file.readlines()
		file.close()
	ue_list=[]
	zsid=[]
	parts =[]
	print " **** Checking for all UEs Context in the Log.... *** "
	#Removing Junk Data from Dump file
	for line in lines:
		parts = line.split() # split line into parts
		if len(parts) < 6:  #error logs
			continue
		if len(parts[6])>3:
			continue
		if len(parts) > 6:
			#print parts[6]
			column2 = parts[6]
		ue_list.append(column2)
	
		if column2.isdigit():
			zsid.append(column2)
		try:
			with open('temp.txt', 'a') as f2:
				f2.write(line)
		except IOError:
			print "Error: can\'t find file or read data"
	#Find Unique UE Ids connected to the FAP	
	uniques = []
	#euCount =0
	for item in ue_list:
		if item not in uniques and item.isdigit():
			euCount=euCount + 1
			#print item
			open(item+'.in', 'a')	
			uniques.append(item)
	print uniques
	print "\n Total No Of UEs attached to FAP = %d \n UE IDs" % euCount, uniques
	#Creating Logs per IE		
	arrIndex =-1
	for item in uniques :
		arrIndex +=1
	#writing logs for each UEs
		try :
			file = open('temp.txt', 'r')
		except IOError:
			print "Error: can\'t find file or read data"
		else:
			lines = file.readlines()
		#file.close()
		for line in lines:
			parts = line.split() # split line into parts
			if len(parts) > 0:
				column2 = parts[6]
			if column2 == uniques[arrIndex]:
				with open(column2+'.in', 'a') as f2:
					f2.write(line)
	print "Input Files per UE : "
	for file in os.listdir("./"):
		if file.endswith(".in"):
			print file
	
	#Calling PostProcessing Function
	postP.postProcessing(uniques)															
	return euCount 

if __name__ == '__main__':
	if len(sys.argv)<2:
		print "\nPlease Provide Input Files ..Calling exit!!"
		print '  Usage : main.py  <inputfile>'
		sys.exit(2)
	print "****Post Processing of Input File %s: " % sys.argv[1]
    
	#Calling LogFiles To Remove Log Files
	LogFiles.Logs_Files()
    
	#File_Alignment gives InputDump.txt as Output File
	align.InputAlignment(sys.argv[1])
    
	#Process Dump from Trace_Tool
	euCount=Process_InputDump('InputDump.txt',0)
	print 'Total rnti Connected to FAP = %d \n' % euCount	
	if euCount == 0:
		print 'No UEs context are Found = %s'%euCount
	
	#List All OutPut Files
	LogFiles.ListFiles()
	
	#Combine DL/UL outFiles *.csv
	combine.CombineDLConfig()
	combine.CombineULConfig()
	combine.CombineDLHarq()
	combine.CombineULHarq()
	#Combine DL UL LC SCH and Metrices
	combine.CombineDLlcStats()
	combine.CombineULlcStats()

	#Delete Temp files
	combine.delTemp()	

#end
