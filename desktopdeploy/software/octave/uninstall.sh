#! /bin/bash

## script to install octave 

sudo -E apt-get --force-yes -y purge octave
sudo -E apt-get --force-yes -y purge qtoctave

rm ~/Desktop/qtoctave.desktop
