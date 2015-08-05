#!/usr/bin/python

import re
import os
import sys

from subprocess import call

#Working Files
t1SpaceFile = "/tmp/T1_admin_disk_space.out"
t2SpaceFile = "/tmp/T2_admin_disk_space.out"
spaceReport = "/tmp/space_report.out"

#List of emails to send reports to
emails = "myname@somesite.blah yourname@somesite.blah"

#Servers
listOfServers = ["RS_SERVER1","RS_SERVER2","RS_SERVER3","RS_SERVER4"]

#Class to build isql command line
def isqlCommand(servername):
    return('isql -S'+servername+' -Usa -Pthepassword -w400 -b -o')

#Sets one or more flags based on command line arguments
#No flags -> command will print to STDOUT
#  Mail Flag -> command will email list to designated addressees

if len(sys.argv) > 1:
    if "mail" in sys.argv:
        mail_flag = 1
    else:
        mail_flag = 0
else:
    mail_flag = 0
    

outFile = open(spaceReport,'w')

#Write admin_disk_space.sql file - ensures that file exists when called by isql command
sqlFile = open('admin_disk_space.sql','w')
sqlFile.write("admin disk_space \ngo\n")
sqlFile.close()

sqlInFile = " -iadmin_disk_space.sql"

header = ( "\n    Device      Space Left      Device Size     Space Used    Status\n"
           "-------------------------------------------------------------------------\n")
           
for server in listOfServers:
    connectString = isqlCommand(server)
    outfile.write ("\n%15s" % (server))
    #outfile.write (header)
    spaceFile = ("/tmp/" + server + ".space.out")
    
    iFile = os.popen(connectString + spaceFile + sqlInFile)
    sFile = (open(spaceFile)
    spaceLine = sFile.readlines()
    totalSpace = 0
    totalUsed = 0
    for space in spaceLine:
        reader = space.split()
        useSegs = int(reader[4])
        totalSegs = int(reader[3])
        totalSpace = usedSegs + totalSpace
        totalUsed = usedSegs + totalUsed
        remSegs = totalSegs - usedSegs
#        text = ("%15s  ***  %5d  ***  %10s %10s %15s \n" %
#           (reader[1],remSegs,totalSegs,usedSegs,reader[5]))
#        outFile.write(text)
    if totalSpace > 0:
        pctUsed = (float(totalUsed) * 100 / float(totalSpace))
    else:
        pctUsed = 0
        
    outFile.write("\n%20s %10s %18s \n" % ("Total Space","Used","Percent Used"))
    outFile.write('-'*73)
    outFile.write("\n%20d %10d %15.2f \n" % (totalSpace,totalUsed,pctUsed))
    sFile.close()
    
outFile.close()

outFile = open(spaceReport,'r')

if mail_flag == 0:
    for line in outFile:
        print(line)
    outFile.close()
else:
    os.system('cat /tmp/space_report.out | /usr/bin/mailx -s "Stable Queue Space  " ' + emails)
    os.system('chmod 777 /tmp/space_report.out')
    
def sqlFile(command):
    if command == "sqm":
        sqlFile = open('admin_who.sql','w')
        sqlFile.write("admin who,sqm \ngo\n")
        sqlFile.close()
    elif command == "space":
        sqlFile = open('amdin_disk_space.sql','w')
        sqlFile.write("admin disk space \ngo\n")
        sqlFile.close()
