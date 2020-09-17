
'''
Since you cant just run trim_video.py on a large file (int overflow (i think)). Its necasary to split it up into segments, run trim_video.py on th segments, then recombine them.
'''
'''
import os
import subprocess
import shutil

#the main project dir
mainDir = os.getcwd()
print("mainDir: "+mainDir)
fileList = os.listdir()
#print (fileList)

for f in fileList:
    #an array where the first element is the filename and the secnd is the extension
    #eg test.mp4 => ['test','mp4']
    fNameExt = f.rsplit('.',1)
    #if it has an extension and its an mp4 file
    if (len(fNameExt)>1 and (fNameExt[1]=='mp4')):
        print(f)
        #partition the mp4 into segments of 15 min
        partFileFolder = "partitioned_files["+fNameExt[0]+"]"
        os.system(("mkdir \""+partFileFolder+"\""))
        #a command to spit the file into pieces
        cmd = 'ffmpeg -i \"'+mainDir+'\\'+f+'\" -c copy -map 0 -segment_time 00:05:00 -f segment \"'+mainDir+'\\'+partFileFolder+'\output%03d.mp4\"'
        os.system(cmd)

        #trim the partitioned files
        trimmedFolder = "trimmed_files["+fNameExt[0]+"]"
        os.system("mkdir \""+trimmedFolder+"\"")
        partFileList = os.listdir(partFileFolder)
        for partFile in partFileList:
            #start by checking if there is a temp folder in partFileFolder
            try:
                shutil.rmtree("TEMP")
            except OSError as e:
                print("Error: %s : %s" % ("TEMP", e.strerror))
            inputFilePath = partFileFolder+"\\"+partFile
            #print("input file: "+inputFilePath)
            outputFilePath = trimmedFolder+'\\'+partFile
            #print("output file: "+outputFilePath)
            #a command to trim the silent bits from the segmented mp4 files and save the results in a folder outputFilePath
            cmd = "python trim_video.py --input_file \""+inputFilePath+"\" --output_file \""+outputFilePath+"\""
            #print("command:")
            #print(cmd)
            os.system(cmd)
        #now combine the trimmed parts into one big file
        trimmedFiles = os.listdir(trimmedFolder)
        #print(trimmedFiles)
        #create a text file for ffmpeg to read from when combining a new file
        trimmedFilesListName = "trimmed_list.txt"
        trimmedFilesListTxt = open(os.getcwd()+"\\"+trimmedFilesListName, "w")
        #a string to write to the file.
        trimmedFilesListString = ""
        #add all the files to the string
        for t in trimmedFiles:
            trimmedFilesListString+="file \'"+mainDir+"\\"+trimmedFolder+"\\"+t+"\'\n"
        trimmedFilesListTxt.write(trimmedFilesListString)
        trimmedFilesListTxt.close()
        #now stitch the files together
        cmd = "ffmpeg -f concat -safe 0 -i "+trimmedFilesListName+" -codec copy \"results\\"+fNameExt[0]+"(final).mp4\""
        os.system(cmd)

        #now clean up the intermediate files 
        os.system("del "+trimmedFilesListName)
        #delete the partitioned and trimmed folders
        try:
                shutil.rmtree(trimmedFolder)
        except OSError as e:
            print("Error: %s : %s" % (trimmedFolder, e.strerror))
        try:
                shutil.rmtree(partFileFolder)
        except OSError as e:
            print("Error: %s : %s" % (partFileFolder, e.strerror))
'''

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time

import os
import subprocess
import shutil
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
input("press enter to select a file to remove silent bits.")
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)


inputFilePath = filename.rsplit('/',1)[0]

inputFileName = filename.rsplit('/',1)[1]

print('inputFilePath: '+inputFilePath)
print('inputFileName: '+inputFileName)

#the main project dir
mainDir = inputFilePath
print("mainDir: "+mainDir)
os.chdir(mainDir)


#an array where the first element is the filename and the secnd is the extension
#eg test.mp4 => ['test','mp4']
fNameExt = inputFileName.rsplit('.',1)
#if it has an extension and its an mp4 file
if (len(fNameExt)>1 and (fNameExt[1]=='mp4')):
    print("inputFileName: "+inputFileName)
    #partition the mp4 into segments of 15 min
    partFileFolder = "partitioned_files["+fNameExt[0]+"]"
    os.mkdir((mainDir+"/"+partFileFolder))
    #a command to spit the file into pieces
    cmd = 'ffmpeg -i \"'+mainDir+'\\'+inputFileName+'\" -c copy -map 0 -segment_time 00:05:00 -f segment \"'+mainDir+'\\'+partFileFolder+'\output%03d.mp4\"'
    os.system(cmd)

    #trim the partitioned files
    trimmedFolder = "trimmed_files["+fNameExt[0]+"]"
    os.mkdir(mainDir+"/"+trimmedFolder)
    partFileList = os.listdir(partFileFolder)
    for partFile in partFileList:
        #start by checking if there is a temp folder in partFileFolder
        try:
            shutil.rmtree("TEMP")
        except OSError as e:
            print("Error: %s : %s" % ("TEMP", e.strerror))
        inputFilePath = partFileFolder+"/"+partFile
        #print("input file: "+inputFilePath)
        outputFilePath = trimmedFolder+'/'+partFile
        #print("output file: "+outputFilePath)
        #a command to trim the silent bits from the segmented mp4 files and save the results in a folder outputFilePath
        cmd = "python trim_video.py --input_file \""+inputFilePath+"\" --output_file \""+outputFilePath+"\""
        #print("command:")
        #print(cmd)
        os.system(cmd)
    #now combine the trimmed parts into one big file
    trimmedFiles = os.listdir(trimmedFolder)
    #print(trimmedFiles)
    #create a text file for ffmpeg to read from when combining a new file
    trimmedFilesListName = "trimmed_list.txt"
    trimmedFilesListTxt = open(os.getcwd()+"/"+trimmedFilesListName, "w")
    #a string to write to the file.
    trimmedFilesListString = ""
    #add all the files to the string
    for t in trimmedFiles:
        trimmedFilesListString+="file \'"+mainDir+"/"+trimmedFolder+"/"+t+"\'\n"
    trimmedFilesListTxt.write(trimmedFilesListString)
    trimmedFilesListTxt.close()
    #now stitch the files together
    cmd = "ffmpeg -f concat -safe 0 -i "+trimmedFilesListName+" -codec copy \""+mainDir+"/"+fNameExt[0]+"(final).mp4\""
    os.system(cmd)

    #now clean up the intermediate files 
    os.system("del "+trimmedFilesListName)
    #delete the partitioned and trimmed folders
    try:
            shutil.rmtree(trimmedFolder)
    except OSError as e:
        print("Error: %s : %s" % (trimmedFolder, e.strerror))
    try:
            shutil.rmtree(partFileFolder)
    except OSError as e:
        print("Error: %s : %s" % (partFileFolder, e.strerror))
