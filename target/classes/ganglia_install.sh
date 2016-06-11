#!/bin/sh
echo 'starting to extract installation files...'
sudo tar -xzf ganglia.tar.gz
if [ $? > 0 ];
	then echo 'decompression error, exit';
	exit 0;
fi
#cd ganglia
#sudo ./configure
#sudo make
#sudo make install