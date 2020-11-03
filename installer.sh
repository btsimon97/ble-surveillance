#!/bin/bash
# This is an installation script for the BT Surveillance Framework
# Eventually we hope to do native packages for the OS, but in the meantime,
# This shell script should set up the application for you.
# NOTE: Kismet plugin setup and PyPi dependency loading isn't implmented yet.
# You'll need to do this part manually for now until its added here.

#Begin Script Constants Declaration
PROG_USERNAME=btsurveillance-processing
PROG_GROUPNAME=btsurveillance
#End Script Constants Declaration

if [ `whoami` != root ]; then
	echo This script must be run as root or with sudo for it to work.
	echo Please re-run this script as root or with sudo
	exit
fi

#CHeck if user already exists and abort with error if it does.
USER_LIST="$(getent passwd | cut -d : -f 1)"
if [[ "$USER_LIST" == *"$PROG_USERNAME"* ]]; then
	echo "The username that this program uses already exists."
	echo "Verify that this username isn't being used elsewhere and try again."
	exit
fi

#Check if group already exists and abort with error if it does.
GROUP_LIST="$(getent group | cut -d : -f 1)"
if [[ "$GROUP_LIST" == *"$PROG_GROUPNAME"* ]]; then
	echo "The group that this program uses already exists."
	echo "Verify that this group isn't being used elsewhere and try again."
	exit
fi

#Create the user and group.
useradd btsurveillance-processing
groupadd btsurveillance
groupmems -g btsurveillance -a btsurveillance-processing

#Deploy the tmpfiles config and reload systemd's config
cp bt-surveillance.conf.systemd-tmpfiles /lib/tmpfiles.d/bt-surveillance.conf
systemd-tmpfiles --create --remove --boot

#Install service executable (this will overwrite any existing binary)
cp middleware.py /bin/bt-surveillance
chmod +x /bin/bt-surveillance

#Install the systemd service
cp bt-surveillance.service /etc/systemd/system/
systemctl daemon-reload

#Start the Service
systemctl start bt-surveillance.service

#TODO: Add kismet detection logic and plugin install steps.
#TODO: Add PyPi dependency installation.

#Install is done, provide post-install instructions to user and exit.
echo "Installation Complete!"
echo "The BT surveillance program has been installed and the service is running."
echo "You still need to install kismet and add the plugin to receive data."
echo "See the repo for instructions on how to do this."
