#! /bin/bash
downloadDir=~/.packages ;
export DEBIAN_FRONTEND=noninteractive
sudo -E apt-get update ;
sudo -E apt-get -y upgrade ;
sudo -E apt-get -y install openssh-server ;
#sudo -E apt-get -y install gnome-session ;
sudo -E apt-get -y install ubuntu-desktop ;
#sudo -E apt-get -y install compizconfig-settings-manager ;
sudo -E apt-get -y install gnome-session-fallback ;
if [ ! -d "$downloadDir" ]; then 
    mkdir $downloadDir ;
fi
cd $downloadDir ;
if [ ! -e nxclient_3.5.0-7_amd64.deb ]; then 
    wget http://64.34.173.142/download/3.5.0/Linux/nxclient_3.5.0-7_amd64.deb ;
fi
if [ ! -e nxnode_3.5.0-9_amd64.deb ]; then 
    wget http://64.34.173.142/download/3.5.0/Linux/nxnode_3.5.0-9_amd64.deb ;
fi
if [ ! -e nxserver_3.5.0-11_amd64.deb ]; then 
    wget http://64.34.173.142/download/3.5.0/Linux/FE/nxserver_3.5.0-11_amd64.deb ;
fi

if [ ! -d /usr/NX ]; then
    sudo dpkg -i nxclient_3.5.0-7_amd64.deb ; 
    sudo dpkg --unpack nxnode_3.5.0-9_amd64.deb ;
    sudo /usr/NX/scripts/setup/nxnode --install ;
    sudo dpkg --unpack nxserver_3.5.0-11_amd64.deb ;
    sudo /usr/NX/scripts/setup/nxserver --install ;
    sudo perl -p -i -e 's/EnablePasswordDB = "0"/EnablePasswordDB = "1"/' /usr/NX/etc/server.cfg
    service nxserver restart
fi