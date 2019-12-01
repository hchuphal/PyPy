# Author : Himanshu Chuphal

import os
#import re
import subprocess
if __name__ == "__main__":
    os.system('cls')
    print "*" * 50
    package = 0
    classF = 0
    DIR = './qualyzer/'
    for root, dirs, files in os.walk(DIR):
         for file in files:    
            if file.endswith('.java'):
                classF += 1
    print "Total number of classe(s) found ::"
    print classF
    path, dirs, files = next(os.walk(DIR))
    print "Total number package in the project ::"
    #print len(dirs)
    # prog = re.compile('(?:.*)')
    dirs[:] = [x for x in dirs if ".git" not in x]
    print len(dirs)
    print  dirs
    print "Enter the package name to create the Class Diagram"
    interF = raw_input("interface path/name = ") 
    print "Generating input for Class Diagram...."
    command_1 = 'java -jar plantuml-dependency-cli-1.4.0.jar -b '+ interF + ' -o input.txt'
    #print command_1
    os.system(command_1)
    print "Now Generating the Graph...."
    command_2 = 'java -jar plantuml.jar input.txt'
    os.system(command_2)
    print "Opening the class Diagram...."
    os.system('input.png')
    #os.system('dot -Tpng -O input.txt')
    print "*" * 50

    # Commands
    # java -jar ../plantuml-dependency-cli-1.4.0-jar-with-dependencies.jar -b providers/ -o pro.txt
    # java -jar ../plantuml.jar -o providers/


