#!/bin/sh

INSTALL_DIR="/usr/local/ganglia"
RRDS_DIR="/var/lib/ganglia/rrds"

install_gmetad(){
	echo "starting to install library dependencies [rrdtool, apr, libconfuse, expat]..."
	apt-get install rrdtool librrd-dev -y
	apt-get install libapr1 libapr1-dev -y
	apt-get install libconfuse-dev -y
	apt-get install libexpat1 libexpat1-dev -y
	if [ $? -gt 0 ] 
		then 
		echo "library dependencies installation failed!"
		exit 0
	fi
	echo "library dependencies installation completed, starting to install ganglia components..."
	./configure --prefix=$INSTALL_DIR --with-gmetad
	if [ $? -gt 0 ] 
		then 
		echo "configuration error !"
		exit 0
	fi	
	make && make install
	if [ $? -gt 0 ] 
		then 
		echo "installation failed"
	else
		echo "installation completed"
	fi
}

install_gmond(){
	./configure --prefix=$INSTALL_DIR
	if [ $? -gt 0 ]
		then 
		echo "configuration error !"
	fi
	make && make install
	if [ $? -gt 0 ] 
		then 
		echo "installation failed"
	else
		echo "installation completed"
	fi
}

# init gmetad.conf
init_gmetad_config(){
	if [ ! -e $RRDS_DIR ]
		then
		mkdir -p $RRDS_DIR
	fi
	echo "setuid_username "root"" >> $INSTALL_DIR/etc/gmetad.conf
	$INSTALL_DIR/sbin/gmetad &
	echo "gmetad.conf has been configured successfully"
}

# init gmond.conf
init_gmond_config(){
	$INSTALL_DIR/sbin/gmond -t | tee "$INSTALL_DIR/etc/gmond.conf"
	$INSTALL_DIR/sbin/gmond &
	echo "gmond.conf has been configured successfully"
}

prepare(){
	echo "starting to extract ganglia.tar.gz..."
	tar -xzf ganglia-3.7.1.tar.gz
	if [ $? -gt 0 ] 
		then 
		echo "decompression error !"
		exit 0
	fi
	echo "decompression completed, starting to install ganglia $1 component..."
	cd ganglia-3.7.1
}

install(){
	prepare
	case $1 in
		gmetad)
		install_gmetad
		init_gmetad_config
		init_gmond_config
		;;
		gmond)
		install_gmond
		init_gmond_config
		;;
		*)
		echo "Usage: $0 [ gmetad | gmond ]"
		;;
	esac
}

install $1
