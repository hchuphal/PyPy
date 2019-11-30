#!/usr/bin/env python
#ListFiles.py : Post Processing of TT Logs

import re
import sys
import os
import postP

#Cleaning previous Logs
def Logs_Files():
        for file in os.listdir("./"):
                if file.endswith(".csv") or file.endswith(".in"):
                        os.remove(file)
                if file.startswith("temp.txt"):
                        os.remove("temp.txt")
                if file.startswith("InputDump.txt"):
                        os.remove("InputDump.txt")
                #if file.startswith("dump.txt"):
                 #       os.remove("dump.txt")
        print "\n Removed all Previous Logs! "
        # listing directories
        print "The dir is: %s"%os.listdir(os.getcwd())

#List All OutPut Files
def ListFiles():
	print "All Logs files Generated as .csv per UE Id :"
	for file in os.listdir("./"):
		if file.endswith(".csv"):
			print file
if __name__ == '__main__':
        print "****Logs Files : "
		#print "\n***** Processing TT Dump File : %s ****** "% filename 
