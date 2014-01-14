#! /bin/bash

## script to install octave 

sudo -E add-apt-repository -y ppa:picaso/octave
sudo -E apt-get update  
sudo -E apt-get --force-yes -y install octave
sudo -E apt-get --force-yes -y install qtoctave

