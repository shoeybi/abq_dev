#! /bin/bash

## script to prepare a AWS node with UBUNTU 12.04 for 
## an ABAQUAL desktop

downloadDir=~/.packages ;
export DEBIAN_FRONTEND=noninteractive
## update and upgrade
sudo -E apt-get update ;
sudo -E apt-get -y upgrade ;
## get ssh server ( should be there already )
sudo -E apt-get -y install openssh-server ;
## get the graphical interface tools (gnome) 
sudo -E apt-get -y install gnome-session ;
sudo -E apt-get -y install ubuntu-desktop ;
#sudo -E apt-get -y install compizconfig-settings-manager ;
sudo -E apt-get -y install gnome-session-fallback ;

echo "%sudo ALL=(ALL)  NOPASSWD: ALL" | sudo tee -a /etc/sudoers

## download and install NX
if [ ! -d "$downloadDir" ]; then 
    mkdir $downloadDir ;
fi
cd $downloadDir ;

if [ ! -e nomachine-workstation_4.0.314_1_beta2_amd64.deb ]; then
    wget http://64.34.173.142/download/4.0/Linux/nomachine-workstation_4.0.314_1_beta2_amd64.deb
fi

#if [ ! -e nomachine-enterprise-server_4.0.312_7_beta2_amd64.deb ]; then
#    wget http://64.34.173.142/download/4.0/Linux/nomachine-enterprise-server_4.0.312_7_beta2_amd64.deb
#fi

if [ ! -e nomachine-portal-server_4.0.314_1_beta2_amd64.deb ]; then
    wget http://64.34.173.142/download/4.0/Linux/nomachine-portal-server_4.0.314_1_beta2_amd64.deb ;
fi



if [ ! -d /usr/NX ]; then
    
    sudo dpkg -i nomachine-workstation_4.0.314_1_beta2_amd64.deb ;
    sudo dpkg -i nomachine-portal-server_4.0.314_1_beta2_amd64.deb ;
#    sudo dpkg -i nomachine-portal-server_4.0.312_8_beta2_amd64.deb ;
## enable password for users

#    sudo perl -p -i -e 's/EnablePasswordDB 0/EnablePasswordDB 1/' /usr/NX/etc/server.cfg 
    sudo service nxserver restart
fi


#if [ ! -e nxclient_3.5.0-7_amd64.deb ]; then 
#    wget http://64.34.173.142/download/3.5.0/Linux/nxclient_3.5.0-7_amd64.deb ;
#fi
#if [ ! -e nxnode_3.5.0-9_amd64.deb ]; then 
#    wget http://64.34.173.142/download/3.5.0/Linux/nxnode_3.5.0-9_amd64.deb ;
#fi
#if [ ! -e nxserver_3.5.0-11_amd64.deb ]; then 
#    wget http://64.34.173.142/download/3.5.0/Linux/FE/nxserver_3.5.0-11_amd64.deb ;
#fi

#if [ ! -d /usr/NX ]; then
#    sudo dpkg -i nxclient_3.5.0-7_amd64.deb ; 
#    sudo dpkg --unpack nxnode_3.5.0-9_amd64.deb ;
#    sudo /usr/NX/scripts/setup/nxnode --install ;
#    sudo dpkg --unpack nxserver_3.5.0-11_amd64.deb ;
#    sudo /usr/NX/scripts/setup/nxserver --install ;
## enable password for users
#    sudo perl -p -i -e 's/EnablePasswordDB = "0"/EnablePasswordDB = "1"/' /usr/NX/etc/server.cfg
#    service nxserver restart
#fi

touch ~/.NX_setup_complete
sudo reboot