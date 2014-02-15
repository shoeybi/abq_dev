#! /bin/bash
soft=octave

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

sudo -E add-apt-repository -y ppa:picaso/octave
sudo -E apt-get update  
sudo -E apt-get --force-yes -y install octave
sudo -E apt-get --force-yes -y install qtoctave

echo "package $soft" | tee -a /home/ubuntu/.packages/installed 
rm /home/ubuntu/.packages/.lockinstall 