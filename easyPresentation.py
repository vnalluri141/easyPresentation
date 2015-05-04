 # !/usr/bin/python
 # This tool converts text file to a html looks like a presenation.

 # -*- coding: utf-8 -*-
 # Version 1.0 05/01/2015
 
 # ***************************************************************************
 # *   Copyright (C) 2015, Varun Srinivas Chakravarthi Nalluri               *
 # *                                                                         *
 # *   This program is free software; any one can redistribute it and/or     *
 # *   modify it under the terms of the GNU General Public License as 	     *
 # *   published by the Free Software Foundation; either version 2 of the    *
 # *   License, or (at your option) any later version.                       *            *
 # *                                                                         *
 # *   This program is distributed in the hope that it will be useful,       *
 # *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 # *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  *
 # *                                                                         *
 # *   Purpose : This program accepts a text file and few arguments as       *
 # *   input and generates a output folder, which contains a html file and   *
 # *   its supporting files like js, css etc. This html file contains the    *
 # *   presentation in the form of html content, which can be opened with    *
 # *   any browser.                                                          *
 # *                                                                         *
 # ***************************************************************************


import os
import sys
import getopt
import codecs
import shutil
import markdown
import tempfile

from subprocess import Popen, PIPE

def main(argv):
    template_id = 1
    custom_markdown_args = ""
    path = "output" + os.path.sep
    input_file_name = ""
    input_textfile_path = ""
    out_file_name = "easyPresentation.html"
    argc = len(argv)

    # checking if minimum number of arguments required passed
    if argc < 1:
        print ("Inavlid number of arguments passed\n")
        print ("Please use -h or --help for help")
        sys.exit(2)

    # Reading path of program being run
    meta_path = os.path.dirname(os.path.abspath(sys.argv[0])) + os.path.sep

    # Reading passed arguments
    try:                                
        opts, args = getopt.getopt(argv, 'h:o:t:f:m:d', ["help", "outpath=","template=","filename=","markdown="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)   

    if len(args) > 0:
        input_file_name = args[0]
    else:
        print ('No input text file given in arguments, input text file is mandatory')
        print ('use -h or --help for getting help')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ('-m',"--markdown"):
            # (kp) use consistent space around operators. if '=' has spaces around it, so should '+'
            custom_markdown_args = arg
            print("Custom markdown call identified...")
        elif opt in ('-o',"--outpath"):
            path = arg
            # reqChangePath(arg)
        elif opt in ('-t',"--template"):
            template_id = arg
        elif opt in ('-f',"--filename"):
            out_file_name = arg
        else:
            print ('unhandled option %s',opt)

    # checking if non optional arguments are passed.
    if input_file_name == "":
        print ('No input text file given in arguments, input text file is mandatory')
        print ('use -h or --help for getting help')
        sys.exit(2)

    input_textfile_path = os.path.dirname(os.path.abspath(input_file_name)) + os.path.sep
    # opening input txt file
    f = open(input_file_name,"r")

    # Loading template configuration
    templateConfig = load_config(template_id,meta_path)

    # reqChangePath(path)
    # copying all the required files to output path specified
    path = copy_files(meta_path + templateConfig["Template path"], path, templateConfig["Template name"])
    if templateConfig == {}:
        print ("SYS ERR :: INVALID TEMPLATE ID")
        sys.exit(1)
    # reading the template file
    template = open (meta_path + templateConfig["Template path"] + templateConfig["Template name"],"r")

    htmlContent = template.read()

    # This is very important. This  perticular string should be present in template and this is where all the generated div blocks need to be placed
    htmlDataPart1, htmlDataPart2 = htmlContent.split('--slide content--', 1)
    index = htmlDataPart1.find("</head>")
    if index == -1:
        index = htmlDataPart1.find("<body")
    htmlDataPart1 = htmlDataPart1[:index] + " <link rel=\"stylesheet\" type=\"text/css\" href=\"css/slideCustomCSS.css\"> " + htmlDataPart1[index:]
    template.close()
    data = f.read()
    
    # Formatting the input text and converting it to html
    addStyles(data, path, input_textfile_path)
    data = data[data.find("~slidestart"):]
    data = convertTextToHtml(data, custom_markdown_args)
    data = data.replace("~slidestart",templateConfig["current slide"],1)
    data = data.replace("~slidestart",templateConfig["all slides"])
    data = data.replace("~slideend","</div>")
    data = data.replace("\~slidestart","~slidestart")
    data = data.replace("\~slideend","~slideend")
    output = convertTextToHtml(data, custom_markdown_args)

    # writing all the changes to output file
    output = htmlDataPart1 + output + htmlDataPart2
    output_file = codecs.open(path+out_file_name, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(output)

    # Close the file
    f.close()

# Opens a file 
def open_file(file_name, mode):
    file_content = None
    try:
        file_content = open(file_name, mode)
    except (OSError, IOError) as e:
        print('Error occured while opening file.\n Error: %s' % e)
    return file_content

# print directions to use this tool
def usage():
    print ("Usage: python3 easyPresentation.py [OPTIONS] <input_filename>")
    print ("   Note: All the optional arguments must be given before input text file.\n")
    print ("-h, --help \t\t display this help and exit")
    print ("-o, --outpath \t\t Copy all output files to specified path, \n\t\t\t if no path is specified by default 'outfolder' will be created in current directory")
    print ("-f, --filename \t\t change primary out put file name")
    print ("-t, --template \t\t select template")
    print ("-m, --markdown \t\t specify custom markdown text to html conversion tool\n")
    print ("Sorry for the mess, I'm still under development!!")


# Identifying path related special characters and resolving obsolute path, I am not  sure if this is needed. But still keeping this for later use
def reqChangePath(path):
    # (kp) this check is wrong. hidden files on unix filesystems start with '.' so startswith('.') is not a good check for current directory
    # (kp) this is actually the same bug that Ken Thompson had in the original unix impl of the filesystem which lead to dotfiles being hidden in the first place
    if path.startswith('.') or path.startswith('~'):
        p = Popen("pwd", stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        if rc != 0:
            print("Invalid cmd")
        else:
            path = output + path[1.]

    if not os.path.exists(path):
        os.makedirs(path)

# Read configuration of selected templete
def load_config(tnum, file_loc):
    flag = 0
    templateConfig = {}
    templet = open_file (file_loc+"config","r")
    for line in templet :
        if line.strip().startswith("Template id") and flag == 1 :
            return templateConfig
        if line.strip().startswith("Template id") and flag == 0 :
            if int(tnum) == int(line.split(':',1)[1].strip()):
                flag = 1
        if flag == 1 and line.strip() != "":
            key = line.split(':',1)[0].strip()
            value = line.split(':',1)[1].strip()
            if key == "current slide" or key == "all slides":
                value = value[:value.find('>')] + " class=\"customSlideCSS\" " + ">"
             #   value = value + "<div class=\"customSlideCSS\">"
            templateConfig[key] = value
    return templateConfig

# Ignore specified files while copying
def ignore_function(ignore):
    def _ignore_(path, names):
        ignored_names = []
        if ignore in names:
            ignored_names.append(ignore)
        return set(ignored_names)
    return _ignore_

# Copy all files from source to destination
def copy_files (src, dest, tname):
    try:
	# Checking if user selected destination directory is already exists
        while os.path.exists(dest):
            print ('destination directory '+dest+' already exits!!')
            is_delete = input("Enter 'Y' to replace directory or 'N' to enter new destination path (Y/N): ")
            if is_delete.upper() == 'Y':
                shutil.rmtree(dest)
            else:
                dest = input('Enter new destination path to continue : ')	# Reading new destination path
        shutil.copytree(src, dest, ignore=ignore_function(tname))
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            print('Directory not copied. Error: %s' % e)
    return dest

# Creating CSS style class. Need to include CSS3 functionalities.
def addStyles(rawText, path, input_file_path):
    preDefCSS = initStyles()
    if not path.endswith(os.path.sep):
        path = path + os.path.sep
    if not os.path.exists(path + "css" + os.path.sep ):
        os.makedirs(path + "css" + os.path.sep)
    customCSS = open_file (path+"css" + os.path.sep + "slideCustomCSS.css",'w')
    customCSS.write(".customSlideCSS { ")    
    styletext = rawText.split('~slidestart',1)[0]
    if styletext != "":
        styletext = styletext.replace("[","")
        styletext = styletext.replace("]",";")
        styles = styletext.split(";")
        for style in styles:
            if style.strip() != "":
                key,value = style.split(':',1)
                key = key.strip()
                value = value.strip()
                if key == "bgimage":
                    # Creating a folder inside css folder and copying back-ground image into that folder.
                    if not os.path.exists(path + "css" + os.path.sep + "bgimages" + os.path.sep):
                        os.makedirs(path+"css" + os.path.sep + " bgimages" + os.path.sep)
                    shutil.copy(input_file_path+value, path + "css" + os.path.sep + "bgimage")
                    value = "url(\"bgimage\")"
                customCSS.write("{0} : {1};".format(preDefCSS[key],value))
    customCSS.write("}")
    customCSS.close()
        
# Initiating basic styles defined for this tool. We can add attribute to below list and use it. 
def initStyles():
    preDefCSS = {}
    preDefCSS["bgimage"] 	= "background-image"
    preDefCSS["bgcolor"] 	= "background-color"
    preDefCSS["bgimage-repeat"] = "background-repeat"
    preDefCSS["text-color"] 	= "color"
    preDefCSS["font"] 		= "font"
    preDefCSS["font-size"] 	= "font-size"
    preDefCSS["bgimage-size"] 	= "background-size"
    preDefCSS["left-margin"] 	= "padding-left"
    preDefCSS["top-margin"] 	= "padding-top"
    preDefCSS["bottom-margin"] 	= "padding-bottom"
    preDefCSS["right-margin"] 	= "padding-right"
    return preDefCSS 
    
# Converts markdown text to html text
def convertTextToHtml(data, custom_markdown_args):
    output = ""
    if custom_markdown_args == "":
        output = markdown.markdown(data)					# Using imported python markdown 
    else:     
        if ' ' in custom_markdown_args:
            markdown_cmd = custom_markdown_args.split(' ', 1)[0]		# Using custome markdown argument passed through command line
            markdown_arguments = custom_markdown_args.split(' ', 1)[1] + " "
        else:
            markdown_cmd = custom_markdown_args
            markdown_arguments = " "
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(bytes(data,'UTF-8'))
            temp.flush()
        print("markdown_cmd : %s"% markdown_cmd, "markdown_args : %s"% markdown_arguments)
        p = Popen(["markdown", markdown_arguments+temp.name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        temp.close()
        os.unlink(temp.name)
        if rc != 0:
            print (" Invalid markdown script!")
            if err != "":
                print(" Error while running markdown script : ")
                print(err)
            sys.exit(1)
        else:
            output = output.decode('utf-8')
    return output

# begin main()
if __name__ == "__main__":
    main(sys.argv[1:])
