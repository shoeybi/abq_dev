#! /bin/bash

soft=paraview

counter=0
while [ -f /home/ubuntu/.packages/.lockinstall ]; do 
    sleep 10
    let counter=$counter+1
    if [ "$counter" -eq 10 ]
    then
	rm /home/ubuntu/.packages/.lockinstall ;
    fi
done

touch /home/ubuntu/.packages/.lockinstall 

## script to install octave 

sudo -E apt-get --force-yes -y purge paraviewopenfoam3120

rm /home/ubuntu/.packages/.lockinstall 

sed -i "/$soft/d" /home/ubuntu/.packages/installed 
rm /home/ubuntu/.packages/.lockinstall 