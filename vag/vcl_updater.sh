#!/bin/bash
BACKUPDIR="/etc/varnish/backup/"
AGENTDIR="/var/lib/varnish-agent/"
VCLDEFAULT="/etc/varnish/default.vcl"
LOGFILE="/var/log/vag/vcl.log"
AGENTVCL=$(find $AGENTDIR -mtime -1 -type f \( -iname \*.vcl ! -iname boot.vcl \) -exec ls -t1 {} \; | sed '1!d' )

# backup default vcl
cp $VCLDEFAULT $BACKUPDIR/$(date +%Y%m%d%H%M).vcl

if [ $? -eq 0 ]; then
	echo "Backup OK - $(date +%Y/%m/%d-%H:%M:%S)" | tee -a $LOGFILE
else
	echo "Backup ERROR - $(date +%Y/%m/%d-%H:%M:%S)" | tee -a $LOGFILE
	exit 2
fi

# find new file and copy to default vcl
cp $AGENTVCL $VCLDEFAULT &>/dev/null

if [ $? -eq 0 ]; then
	echo "Copy OK - $(date +%Y/%m/%d-%H:%M:%S)" | tee -a $LOGFILE
else
	echo "Copy ERROR - $(date +%Y/%m/%d-%H:%M:%S)" | tee -a $LOGFILE
	exit 2
fi

# remove old configs
find $BACKUPDIR -cmin +640 -exec rm -fv {} \;

exit 0
