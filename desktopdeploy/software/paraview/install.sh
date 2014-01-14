#! /bin/bash

## script to install openfoam on UBUNTU 12.04
## http://openfoam.org/download/ubuntu.php

# add OpenFOAM to the list of repository locations for apt to search
VERS=$(lsb_release -cs) 
sudo sh -c "echo deb http://www.openfoam.org/download/ubuntu $VERS main > /etc/apt/sources.list.d/openfoam.list"

# Update the apt package list to account for the new download repository location
sudo -E apt-get update

# Install Paraview (3120 in the name refers to version 3.12.0):
sudo -E apt-get --force-yes -y install paraviewopenfoam3120


