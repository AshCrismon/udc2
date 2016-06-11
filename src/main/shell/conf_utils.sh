#!/bin/sh

INSTALL_DIR=/usr/local/ganglia

specificy_cluster(){
	line_start="cluster {"
	line_end="}"
	cmd="/$1 \=/s/\"[a-zA-Z0-9]*\"/\"$2\"/g;p"
	sed -n "/$line_start/,/$line_end/{$cmd}" $INSTALL_DIR/etc/gmond.conf
}

if [ -n "$1" -a -n "$2" ]
then
	specificy_cluster $1 $2
else
	echo "Userage: $0 key value"
	exit 0
fi
