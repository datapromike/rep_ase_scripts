#!/usr/bin/python

import re
import os
import sys
import time

from subprocess import call

#List of DBID:qType to include in abreviated list
## Site Specfic
t1Include = ['101:0','102:1','103:0','104:0','105:0']
t2Include = ['102:0','102:1','103:0','103:1','105:0','1677770:0']

#Working Files
abrevFile = "/tmp/admin_who_check.out"
fullFile = "/tmp/admin_who_check_full.out"
t1SqmFile = "/tmp/T1_admin_who.out"
t2SqmFile = "/tmp/T2_admin_who.out"

#List of email addresses to send reports to
emails = "myemail@somesite.blah yourmail@othersite.blah"

#Sets One or more flags from command line
#No flags -> command will print abreviated Queue list to STDOUT
#  Mail Flag -> command will email abreviated Queue List
#  Full Flag - command will print full Queue List to STDOUT
#  Full + Mail - Command will email full Queue List

if len(sys.argv) > 1:
    if "mail" in sys.argv:
        mail_flag = 1
    else:
        mail_flag = 0
    if "full" in sys.argv:
        full_flag = 1
    else:
        full_flag = 0
else:
    mail_flag = 0
    full_flag = 0
    
outFile = open(abrevFile,'w')
outFile2 = open(fullFile,'w')

#Write admin_who.sql file.  Ensure that it exists when called by isql command
sqlFile = open('admin_who.sql;,'w')

sqlFile.write("admin who,sqm \ngo\n")

sqlFile.close()

header = ( "\n    Queue#        Servername.Database                Queue Size        First      Last\n"
           "---------------------------------------------------------------------------------------\n")

#Write Headers for Abreviated queue list
outFile.write(time.ctime())
outFile.write(%40s" % ("Tier 1"))
outFile.write(header)
#Write Headers for Full queue list
outFile2.write(time.ctime())
outfile2.write("%40s" % ("Tier 1"))
outFile2.write(header)

ft1 = os.system('isql -SRS_SERVERNAME_HERE -Usa -Pthepassword -w400 -b -iadmin_who.sql -o'+ t1SqmFile)
t1_file = open('/tmp/T1_admin_who.out','r')

t1 = t1_file.readlines()

for sqm in t1:
    reader = sqm.split()
    firstBlock = float(reader[-5])
    lastBlock = float(reader[-4])
    queue_size lastBlock - firstBlock
    text = ("%10s %35s   ***  %5d  ***  %10s %10s \n" %
        (reader[-16],reader[-15],queue_size,reader[-5],reader[-4]))
    outFile2.write(text)
    if reader[-16] in t1Include:
        outFile.write(text)

#Write Headers for Abreviated queue list
outFile.write ("\n\n %40s" % ("Tier 2"))
outFile.write (header)
#Write Headers for Full queue list
outFile2.write ("\n\n %40s" % ("Tier 2"))
outFile2.write (header)

ft2 = (os.system('isql -SRS_SERVERNAME2_HERE -Usa -Pthepassword -w400 -b -iadmin_who.sql -o' + t2SqmFile)
t2_file = open('/tmp/T2_admin_who.out','r')
t2 = t2_file.readlines()

for sqm in t2:
    reader = sqm.split()
    firstBlock = float(reader[-5])
    lastBlock = float(reader[-4])
    queue_size = lastBlock - FirstBlock
    text = ("%10s %35s   ***  %5d  ***  %10s %10s \n" %
        (reader[-16],reader[-15],queue_size,reader[-5],reader[-4]))
    outFile2.write(text)
    if reader[-16] in t2Include:
        outFile.write(text)
        
outFile.write("\n")

outFile.close()
outFile2.close()
t1_file.close()
t2_file.close()

if full_flag == 0:
    outFile = open(abrefFile,'r')
else:
    outFile = open(fullFile,'r')

if mail_flag == 0:
    for line in outFile:
        print(line)
    outFile.close()
else:
    if full_flag == 0:
        os.system('cat /tmp/admin_who_check.out | /usr/bin/mailx -s"Replication Queues  " ' + emails)
        os.system('chmod 777 /tmp/admin_who_check.out')
    else:
        os.system('cat /tmp/admin_who_check.out | /usr/bin/mailx -s "Replication Queues  " ' + emails)
        os.system('chmod 777 /tmp/admin_who_check_full.out')
outFile.close()
os.system('rm /tmp/admin_who_check.out')
os.system('rm /tmp/admin_who_check_full.out')

######
#  SQL script file creation 
#####

def sqlFile(command):
    if command == "sqm":
        sqlFile = open('admin_who.sql','w')
        sqlFile.write("admin who,sqm \ngo\n")
        sqlFile.close()
    elif command == "space":
        sqlFile = open('admin_disk_space.sql','w')
        sqlFile.write("admin disk space \ngo\n")
        sqlFile.close()

def isqlCommand(servername)
    return('isql -S'+servername+' -Usa -Pthepassword -w400 -b -o')
    
