##############################################################################################
#
# Description : DevTool Python tool high  level class diagram from a code base 
# Input  : code base home dir or package path
# Output :  Class Diagrams in PNG
# Usage : python2.7 dev_tool.py
# Author : Group 3
#
##############################################################################################

# -*- coding: utf-8 -*-
import json
import os
import re
from texttable import Texttable
from collections import OrderedDict
from collections import defaultdict
import subprocess
import sys
from subprocess import call
from bunch import Bunch
from time import sleep

import inspect

class Formats:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_input(msg, convert_func):
    try:
        value = raw_input(msg)
        if convert_func is not None:
            value = convert_func(value)
    except ValueError:
        value = None
    return value

def valid_int(number):
    if number.isdigit():
        return number
    else:
        raise ValueError

def get_input(msg, name, validate_func, convert_func=None):
    value = read_input(msg, convert_func)
    while not validate_func(value):
        print "Invalid {}".format(name)
        value = read_input(msg, convert_func)
    return value


def get_base_app_directories():
    import master
    base = inspect.getfile(master).split("scripts/code_generator")[0]
    directories = {
        'BASE': base,
        'SON_INIT': "{}{}".format(base, "dist/debian-init.sh")
    }
    return directories


def str_to_bool(string):
    if string in ['YES', 'Y']:
        return True
    elif string in ['NO', 'N']:
        return False
    else:
        raise ValueError

def valid_apps(apps):
    if len(apps) == 0:
        return True
    return all(map(lambda x: x in app_names, apps))


def string_to_list_of_strings(string):
    if string == '':
        return []
    return map(lambda s: s.strip(), string.split(','))


def map_strings_to_list_of_strings(strings):
    return "'{}'".format("','".join(strings))

def _banner(message):
    table = Texttable()
    table.set_deco(Texttable.BORDER)
    table.add_rows([[message]])
    return table.draw()

# Main function which takes the input like APP or infra and perform the actions accordingly
def main():
    os.system('cls')
    print
    print
    print _banner((Formats.OKGREEN + '\n    Software Evolution Project, DAT265/DIT598 - 2019       \n \n DEV TOOL -- Group_3 \n').center(50)) + Formats.ENDC
    print
    print
    _main_menu()

def _main_menu():
    print Formats.WARNING + "Welcome : Input options to create High-Level Class Diagrams >> " + Formats.ENDC
    print
    print Formats.WARNING +" Select an option to create a Class Diagram at diffferent level of abstraction>> " + Formats.ENDC
    print Formats.WARNING + "1. Project Level >> " + Formats.ENDC
    print Formats.WARNING + "2. Package Level - Multiple Packages" + Formats.ENDC
    print Formats.WARNING + "3. Package Level - Individual Package" + Formats.ENDC
    print Formats.WARNING + "4. Class Level - within a Package " + Formats.ENDC
    print Formats.WARNING + "5. Check Version of the tool" + Formats.ENDC
    print Formats.WARNING + "6. -- Help??" + Formats.ENDC
    print Formats.WARNING + "7. EXIT " + Formats.ENDC
    print
    print

    _option = get_input(Formats.OKGREEN +"Enter an option to run the tool [ 1-8 ] = "+ Formats.ENDC,
                     "Invalid Option, Check menu options and select a valid choice!!",
                     lambda x: x>0,
                     valid_int)

    print Formats.WARNING + " >> Enterted Choice : {}".format(_option) + Formats.ENDC
    _menu = {
        '1' : _run_high_level,
        '2' : _mul_packages,
        '3' : _ind_package,
        '4' : _class_package,
        '5' : _check_version,
        '6' : _help_,
        '7' : _quit
    }

    _menu[_option]()
    print


def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()

def _quit():
    exit(0)

def _mul_packages():
    print
    print
    os.system('cls')
    print "*" * 50
    package = 0
    classF = 0
    print "Enter the path of the project home directory"
    DIR = raw_input("Project Full Path = ") 
    #DIR = './qualyzer/'
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
    package_dir = 'cd '+ DIR +''
    print package_dir
    os.system(package_dir)
    print "Enter the Multiple Package names seperated comma(,)"
    interF = raw_input("Package names = ") 
    pack_list = list(interF.split(",")) 
    for i in pack_list: 
        print "Generating input for Class Diagram...."
        command_1 = 'java -jar plantuml-dependency-cli-1.4.0.jar -b '+ DIR+'/'+ i + ' -o '+ i +'.txt'
        print command_1
        os.system(command_1)
    [s + '.txt' for s in pack_list]
    pack_list
    print "Now Generating the Graph...."
    for i in pack_list:
        command_2 = 'java -jar -DPLANTUML_LIMIT_SIZE=81920 plantuml.jar '+ i +'.txt'+ ''
        print command_2
        os.system(command_2)
        print "Opening the class Diagram...."
        os.system(''+ i +'.png')
    #os.system('dot -Tpng -O input.txt')
    print "*" * 50
    print
    print
    _main_menu()

def _ind_package():
    print
    print
    os.system('cls')
    print "*" * 50
    package = 0
    classF = 0
    print "Enter the path of the project home directory"
    DIR = raw_input("Project Full Path = ") 
    #DIR = './qualyzer/'
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
    interF = raw_input("Package path/name = ") 
    print "Generating input for Class Diagram...."
    command_1 = 'java -jar plantuml-dependency-cli-1.4.0.jar -b '+ DIR+'/'+interF + ' -o input.txt'
    #print command_1
    os.system(command_1)
    print "Now Generating the Graph...."
    command_2 = 'java -jar -DPLANTUML_LIMIT_SIZE=81920 plantuml.jar input.txt'
    os.system(command_2)
    print "Opening the class Diagram...."
    os.system('input.png')
    #os.system('dot -Tpng -O input.txt')
    print "*" * 50
    print
    print
    _main_menu()

def _class_package():
    print
    print
    os.system('cls')
    print "*" * 50
    package = 0
    classF = 0
    print "Enter the path of the project home directory"
    DIR = raw_input("Project Full Path = ") 
    #DIR = './qualyzer/'
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
    interF = raw_input("Package path/name = ") 
    print "Enter the classe(s) names or pattern to exclude ="
    classN = raw_input("Class name or pattern = ")
    #class_list = list(classN.split(",")) 
    print "Generating input for Class Diagram...."
    exclude = '*'+classN+'*.java'
    command_1 = 'java -jar plantuml-dependency-cli-1.4.0.jar -b '+ DIR+'/'+interF + ' -o input.txt -e '+ exclude + ' '
    #-e *Code*.java
    print command_1
    os.system(command_1)
    print "Now Generating the Graph...."
    command_2 = 'java -jar -DPLANTUML_LIMIT_SIZE=81920 plantuml.jar input.txt'
    os.system(command_2)
    print "Opening the class Diagram...."
    os.system('input.png')
    #os.system('dot -Tpng -O input.txt')
    print "*" * 50
    print
    print
    _main_menu()

def _check_version():
    command_1 = 'java -jar plantuml.jar -version'
    #print command_1
    os.system(command_1)
    _main_menu()

def _help_():
    command_1 = 'java -jar plantuml.jar -help'
    #print command_1
    os.system(command_1)
    _main_menu()



def _run_high_level():
    print
    print
    os.system('cls')
    print "*" * 50
    package = 0
    classF = 0
    print "Enter the path of the project home directory"
    DIR = raw_input("Project Full Path = ") 
    #DIR = './qualyzer/'
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
    print "Generating input for Class Diagram...."
    command_1 = 'java -jar plantuml-dependency-cli-1.4.0.jar -b '+ DIR + ' -o input.txt'
    #print command_1
    os.system(command_1)
    print "Now Generating the Graph...."
    command_2 = 'java -jar -DPLANTUML_LIMIT_SIZE=81920 plantuml.jar input.txt'
    os.system(command_2)
    print "Opening the class Diagram...."
    os.system('input.png')
    #os.system('dot -Tpng -O input.txt')
    print "*" * 50
    print
    print
    _main_menu()


def _run_package_level(_vendor, _tech, _input_file, _input_xml, _module_name):
    pass

if __name__ == '__main__':
    main()
