#!/usr/bin/ksh
#
#################################################
#
#	rep_check.ksh
#
#	Purpose:  Script will log into the dataserver
#		and query the rs_lascommit
#		table for either a normal or bridge 
#		connection, and report when the most
#		recent transaction was recieved, and
#		the approximate time since the last
#		transaction.
#
#################################################

#########  LOCALLY SET VARIABLES #################
SYBASE=		#location of Sybase Software directory
DSQUERY=		#Server to isql into
USER=sa		#Can use any user with select priveledges on the rs_* tables
RS_TABLE=		#Name of rs_lastcommit table you wish to query
DB_NAME=    #Name of Database to monitor for transactions
######### END LOCALLY SET VARIABLES ##############
source $SYBASE/$SYBASE.sh

#Must have at least one argument
if [ $# -lt 1 ]; then
	echo "Usage:  $0 {password} [all]"
	echo "where password is the password to the database"
	echo "you are querying from."
	echo "Use the  all  option to get the verbose output"
	return 1; exit
fi
#Change Arguments to meaningful names
PASSWD=$1
FLAGS=$2

#Set Sybase Environment
if [ -e $SYBASE/SYBASE.sh ]; then
	. $SYBASE/SYBASE.sh
else
	. $SYBASE/$SYBASE_ASE/SYBASE.sh
	. $SYBASE/$SYBASE_OCS/SYBASE.sh
else
  echo "Unable to set Sybase Environment:  Please check that Sybase home"
  echo "directory is properly set"
  return1; exit
fi

#If flag is 'all' use long output. otherwise just print the time since last tran
if [[ $FLAGS == "all" ]]; then
	isql -U${USER} -P${PASSWD} -S${DSQUERY} -w400 <<ENDSQL
set nocount on
print ""
print ""
declare @c datetime
select @c = max(dest_commit_time) from ${DB_NAME}..${RS_TABLE}
select origin as "Source ID", origin_time as "Source Commit Time",
dest_commit_time as "Local Commit Time",
getdate() as "Current Date and Time"
from ${DB_NAME}..${RS_TABLE}
where dest_commit_time = @c
select datediff(mi, @c, getdate()) as "Minutes Since Last Transaction"
print""
go
ENDSQL
else
	isql -U${USER} -P${PASSWD} -S${DSQUERY} -w400 <<ENDSQL
set nocount on
print ""
print ""
declare @c datetime
select @c = max(dest_commit_time) from ${DB_NAME}..${RS_TABLE}
select datediff(mi, @c, getdate()) as "Minutes Since Last Transaction"
print ""
go
ENDSQL
fi
