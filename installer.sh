#!/bin/bash
# This is an installation script for the BT Surveillance Framework
# Eventually we hope to do native packages for the OS, but in the meantime,
# This shell script should set up the application for you.

#Begin Script Constants Declaration
PROG_USERNAME=bluemon
PROG_GROUPNAME=bluemon
KISMET_APT_PKGS="kismet"
PIP_APT_PKGNAME=python3-pip
KISMET_PIP_PKGNAME=kismetexternal
#End Script Constants Declaration

# cd to script location so file copy commands work
cd "${0%/*}"

# Check to make sure being run with root/sudo perms
if [ `whoami` != root ]; then
	echo "This script must be run as root or with sudo for it to work."
	echo "Please re-run this script as root or with sudo"
	exit
fi

# Check if Kismet and its plugins are installed, install if not present
dpkg -s $KISMET_APT_PKGS > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Installing Kismet Packages..."
	apt install -y $KISMET_APT_PKGS
else
	echo "Kismet Packages already installed, continuing..."
fi

# Check if pip3 is installed, install if not present
dpkg -s $PIP_APT_PKGNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Installing PIP3..."
	apt install -y $PIP_APT_PKGNAME
else
	echo "PIP3 already installed, continuing..."
fi

# Check if kismetexternal pip package is installed, install if not present
# If present, update to latest version.
pip3 show kismetexternal > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Installing kismetexternal python package from pip..."
	pip3 install kismetexternal
else
	echo "Updating installed kismetexernal python package..."
	pip3 install kismetexternal --upgrade --upgrade-strategy=eager
fi

# Check if user already exists, create if it does not

getent passwd $PROG_USERNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Creating user $PROG_USERNAME..."
	useradd $PROG_USERNAME
	chsh -s /sbin/nologin $PROG_USERNAME
fi

#Check if group already exists, create if it does not

getent group $PROG_GROUPNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Creating group $PROG_GROUPNAME..."
	groupadd $PROG_GROUPNAME
fi

#Check if user is member of group, add if not
GROUP_MEMS="$(groupmems -g $PROG_GROUPNAME -l)"
if [[ "$GROUP_MEMS" != *"$PROG_USERNAME"* ]]; then
	echo "Adding $PROG_USERNAME to $PROG_GROUPNAME..."
	adduser $PROG_USERNAME $PROG_GROUPNAME
	#groupmems has a weird quirk with PAM on Debian based OSes, so we use
	#adduser now instead. You can uncomment the groupmems line if you want
	#The old behavior, but remember to comment the adduser line first.
	#groupmems -g $PROG_GROUPNAME -a $PROG_USERNAME
fi

#Deploy the tmpfiles config and reload systemd's config
rm /lib/tmpfiles.d/bt-surveillance.conf
cp bluemon.conf.systemd-tmpfiles /lib/tmpfiles.d/bluemon.conf
systemd-tmpfiles --create --remove --boot

#Install service executable (this will overwrite any existing binary)
rm /bin/bt-surveillance
cp bluemon-kismet.py /bin/bluemon-kismet
cp bluemon-unix.py /bin/bluemon-unix
chmod +x /bin/bluemon-kismet
chmod +x /bin/bluemon-unix

#Install the systemd service
rm /etc/systemd/system/bt-surveillance.service
cp bluemon-kismet.service /etc/systemd/system/
systemctl daemon-reload

#Start the Service
systemctl start bluemon-kismet.service


#Install is done, provide post-install instructions to user and exit.
echo "Installation Complete!"
echo "The BT surveillance program has been installed and the service is running."
